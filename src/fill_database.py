
"""                              _                                    
 _ __  _ __ ___  __ _ _   _  ___| |_ __ ___   ___ _ __ ___   ___  ___ 
| '_ \| '__/ _ \/ _` | | | |/ _ \ | '_ ` _ \ / _ \ '_ ` _ \ / _ \/ __|
| |_) | | |  __/ (_| | |_| |  __/ | | | | | |  __/ | | | | |  __/\__ \
| .__/|_|  \___|\__, |\__,_|\___|_|_| |_| |_|\___|_| |_| |_|\___||___/
|_|                |_|                                                

"""
# All the necessary imports

import os, sys, time
from threading import Thread
import re
import glob

# Separate pip modules/packages

import praw
import pysrt
from tqdm import tqdm, TqdmSynchronisationWarning
import warnings

# Our own scripts

from text_recognition import text_recognition, extract_image
from banlist import banlist
from utils import *
from message import *
import config
import database

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     user_agent=config.user_agent)

subreddit_name = "prequelmemes"
bot_name = f"{subreddit_name}_bot"

subreddit = reddit.subreddit(subreddit_name)

# subreddit = reddit.subreddit('pewds_test')
# If you want to test it out, go to r/pewds_test
# I created this subreddit just for personal testings
# Feel free to use it

subs_dir = "./subtitles/"

checked_file = "./data/checked.txt"

# Just to stop double, triple, QUADRIPLE posting
# An array of checked posts
checked = read_array(checked_file)

def add_zero(string):
    if (len(string) == 1):
        string = f"0{string}"

    return string

def riptime(subrip_time):
    hours = add_zero(str(subrip_time.hours))
    minutes = add_zero(str(subrip_time.minutes))
    seconds = add_zero(str(subrip_time.seconds))
    time_string = f"{hours}:{minutes}:{seconds}"

    return time_string

def replace_chars(text):
    text = re.sub('[^a-zA-Z0-9\n]+', '', text)

    return text

def finish_entry(td):
    print(table(td))
    append_file(logs_file, f"{table(td)}\n\n")

def parse_url(post):

    pattern = re.compile(".(jpe?g|png|gifv?)(\?\S*)?")

    if pattern.search(post.url) is not None:
        return True
    else:
        return False
        
def search_quote(formatted_text, submission):

    for filename in glob.glob(subs_dir + "*.srt"):
        
        subs = pysrt.open(filename)

        for found_word in formatted_text:
            for quote in subs:
                quote_text = quote.text
                quote_text = replace_chars(quote_text).lower()
                quote_text = quote_text.replace("\n","")

                # The reverse text memes are quite popular now.
                # We can easily spot even the inverse quotes.
                if (found_word in quote_text) or (found_word[::-1] in quote_text):
                    citation = quote.text.replace("\n", " ")
                    movie = filename.replace("_", " ").replace(".srt", "").replace(subs_dir, "")
                    start = riptime(quote.start)
                    end = riptime(quote.end)

                    reply = modify_message(citation,
                                           movie,
                                           start,
                                           end
                    )
                    database.insert(submission.id, Quote=citation)
                    return

    database.insert(submission.id)

def submission_thread():

    database.init_database()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", TqdmSynchronisationWarning)
        for submission in tqdm(checked):
            post = reddit.submission(submission)
            
            if (parse_url(post)):
                try:
                    recog_text = text_recognition(extract_image(post)).decode("utf-8").lower()
                except Exception as e:
                    database.insert(post.id)
                    continue
            else:
                database.insert(post.id)
                continue
                
            # Don't get scared from the for loops below
            # They are really small and thus fast
            
            formatted_text = (replace_chars(recog_text).lower().split())[::-1]
            formatted_text = [i for i in formatted_text if len(i) > 8 and not i in banlist]
            
            # If the list is empty, no need for scanning
            if (len(formatted_text) == 0):
                database.insert(post.id)
                continue
            
            # If the main procedure fails, maybe internet connection is down
            # Just wait it out
            try:
                search_quote(formatted_text, post)
            except Exception as e:
                database.insert(post.id)
                continue
                        
def threads():
    Thread(name="Submissions", target=submission_thread).start()

if __name__ == "__main__":
    threads()
