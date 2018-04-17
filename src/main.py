
"""
                                 _                                    
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

from text_recognition import *
from message import message
import config

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     user_agent=config.user_agent)

#subreddit = reddit.subreddit('prequelmemes')
subreddit = reddit.subreddit('prequelmemes')

subs_dir = "./subtitles/"

def riptime(subrip_time):

    hours = subrip_time.hours
    minutes = subrip_time.minutes
    seconds = subrip_time.seconds
    time_string = "{}:{}:{}".format(hours, minutes, seconds)

    return time_string

def reply_post(post, msg):

    post.reply(msg)
    time.sleep(60)

def modify_message(quote, movie, start, end):
    
    reply = message
    reply = reply.replace("%CITATION%", quote)
    reply = reply.replace("%START%", start)
    reply = reply.replace("%END%", end)
    reply = reply.replace("%MOVIE%", movie)

    return reply

def replace_chars(text):
    # This is really bad
    chars = "!@#$%^&*()-_=+,'\";:{}[]\\/`~?.<> "
    for char in chars:
        text = text.replace(char, "")
    return text

def parse_url(post):

    pattern = re.compile(".(jpe?g|png|gifv?)(\?\S*)?")

    if pattern.search(post.url) is not None:
        print("\tMatched the pattern, it has our content.")
        return True
    else:
        return False
        
def search_quote(formatted_text, lines, submission):
    # I will add some comments, 'cause 
    for filename in glob.glob(subs_dir + "*.srt"):
        print(filename)
        
        subs = pysrt.open(filename)

        for i in range(lines):
                
            for quote in subs:
                quote_text = quote.text
                quote_text = replace_chars(quote_text).lower()
                quote_text = quote_text.replace("\n","")
                
                if formatted_text[i] in quote_text:
                    print("Found it!!!\n")
                    print(quote.text)
                    print(quote.start)
                    print(quote.end)
                    reply = modify_message(quote.text.replace("\n", " "),
                                           # I am sorry, bad hack. Will fix.
                                           filename.replace("_", " ").replace(".srt", "").replace(subs_dir, ""),
                                           riptime(quote.start),
                                           riptime(quote.end)
                    )
                    print(reply)
                    reply_post(submission, reply)
                    print("Sent the reply! Will be waiting!!!\n\n\n")
                    return
                    
def submission_thread():

    for submission in subreddit.stream.submissions():

        post = reddit.submission(submission)
        
        print("Parsing post -> {}".format(post.id))

        if (parse_url(post)):
            try:
                recog_text = text_recognition(post).decode("utf-8").lower()
            except Exception as e:
                print("Failed at reading text. Skipping...\n")
                continue
        else:
            print("It is not an image. Skipping...")
            continue
            
        # Don't get scared from the for loops below
        # They are really small and thus fast
        
        formatted_text = replace_chars(recog_text).lower()
        formatted_text = formatted_text.split()
        
        print(formatted_text)
        
        formatted_text = [i for i in formatted_text if len(i) > 8]
        lines = len(formatted_text)

        # If the main procedure fails, maybe internet connection is down
        # Just wait it out
        try: 
            search_quote(formatted_text, lines, submission)
        except Exception as e:
            print("Error occured: {}".format(e))
            time.sleep(600)
            try:
                search_quote(formatted_text, lines, submission)
            except Exception as ee:
                print("Something terrible happened. Can't do it.\n{}".format(ee))
                time.sleep(300)
                continue
            
def save_karma():
    memepolice = reddit.redditor("prequelmemes_bot")
    while True:
        for comment in memepolice.comments.new(limit=100):
            # It will parse 100 comments in 5-6 seconds
            if comment.ups < -2:
                comment.delete()

        # 1 hour of sleep
        time.sleep(3600)
                        
def threads():
    Thread(name="Submissions", target=submission_thread).start()
    Thread(name="Save Karma", target=save_karma).start()

if __name__ == "__main__":
    threads()
