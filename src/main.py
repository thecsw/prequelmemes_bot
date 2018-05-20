

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

# Our own scripts

from text_recognition import text_recognition
from banlist import banlist
from table import table
from utils import *
from message import *
import config

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

counter_file = "./data/counter.txt"
logs_file = "./data/logs.txt"
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

def reply_post(post, msg):
    post.reply(msg)
    time.sleep(60)

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
        
def search_quote(formatted_text, submission, table_data):

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
                    table_data[4] = citation
                    finish_entry(table_data)
                    reply_post(submission, reply)
                    return

    finish_entry(table_data)
                    
def submission_thread():
    counter = (float(read_file(counter_file))) + 1
    for submission in subreddit.stream.submissions():
        table_data = ["None"] * 6

        post = reddit.submission(submission)
        if post.id in checked:
            continue
        checked.append(post.id)
        write_array(checked_file, checked)
        print("\nStarting a new submission...")
        
        table_data[0] = counter
        table_data[1] = post.id
        
        counter+=1
        write_file(counter_file, counter)
        if (parse_url(post)):
            try:
                recog_text = text_recognition(post).decode("utf-8").lower()
                table_data[2] = "Yes"
            except Exception as e:
                table_data[5] = e
                finish_entry(table_data)
                continue
        else:
            table_data[2] = "No"
            finish_entry(table_data)
            continue
            
        # Don't get scared from the for loops below
        # They are really small and thus fast
        
        formatted_text = (replace_chars(recog_text).lower().split())[::-1]
        formatted_text = [i for i in formatted_text if len(i) > 8 and not i in banlist]

        table_data[3] = formatted_text

        # If the list is empty, no need for scanning
        if (len(formatted_text) == 0):
            table_data[3] = "Empty"
            finish_entry(table_data)
            continue
        
        # If the main procedure fails, maybe internet connection is down
        # Just wait it out
        try:
            search_quote(formatted_text, submission, table_data)
        except Exception as e:
            table_data[5] = e
            finish_entry(table_data)
            continue
            
def save_karma():
    memepolice = reddit.redditor(bot_name)
    while True:
        for comment in memepolice.comments.new(limit=100):
            # It will parse 100 comments in 5-6 seconds
            if comment.ups < -2:
                comment.delete()

        time.sleep(1800)
                        
def threads():
    Thread(name="Submissions", target=submission_thread).start()
    Thread(name="Save Karma", target=save_karma).start()

if __name__ == "__main__":
    threads()
