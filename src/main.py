
"""
                                 _                                    
 _ __  _ __ ___  __ _ _   _  ___| |_ __ ___   ___ _ __ ___   ___  ___ 
| '_ \| '__/ _ \/ _` | | | |/ _ \ | '_ ` _ \ / _ \ '_ ` _ \ / _ \/ __|
| |_) | | |  __/ (_| | |_| |  __/ | | | | | |  __/ | | | | |  __/\__ \
| .__/|_|  \___|\__, |\__,_|\___|_|_| |_| |_|\___|_| |_| |_|\___||___/
|_|                |_|                                                
                                                                                                                                                  
"""
import os, sys, time

import praw

import pysrt

from threading import Thread

import re

from text_recognition import *

from message import message

import config

from threading import Thread

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     user_agent=config.user_agent)

subreddit = reddit.subreddit('pewds_test')

pattern = re.compile(".(jpe?g|png|gifv?)(\?\S*)?")

def riptime(subrip_time):
    hours = subrip_time.hours
    minutes = subrip_time.minutes
    seconds = subrip_time.seconds
    time_string = "{}:{}:{}".format(hours, minutes, seconds)
    return time_string

def submission_thread():

    for submission in subreddit.stream.submissions():
        post = reddit.submission(submission)
        
        print("Parsing post -> {}".format(post.id))

        if pattern.search(post.url) is not None:
            print("\tMatched the pattern, it has our content.")
            
            try:
                text = text_recognition(post).lower()
                print("\tText from the image:\t{}\n".format(str(text)))
                if (text.decode("utf-8")) == "":
                    print("Empty string. Continuing")
                    continue

            except Exception as e:
                print(e)
                continue
            
            # Don't get scared from the for loops below
            # They are really small and thus fast
            for (root, dirs, files) in os.walk('./subtitles/'):
                for file_name in files:
                    # file_full_name = ("subtitles/" + file_name).encode("utf-8")
                    subs = pysrt.open("subtitles/{}".format(file_name))
                    for single_sub in subs:
                        if str(text.decode("utf-8")) in (str(single_sub.text)).lower():
                            print("Found the quote!")
                            citation = single_sub.text.replace("\n", " ")
                            start = single_sub.start
                            end = single_sub.end
                            movie = file_name.replace("_", " ")
                            movie = movie.replace(".srt", "")

                            print(citation)
                            print(riptime(start))
                            print(riptime(end))
                            print(movie)

                            reply = message

                            print(reply)
                            
                            reply = reply.replace("%CITATION%", citation)
                            reply = reply.replace("%START%", riptime(start))
                            reply = reply.replace("%END%", riptime(end))
                            reply = reply.replace("%MOVIE%", movie)

                            print(reply)
                            
                            post.reply(reply)
                            time.sleep(30)
                            
                            break
                                           
        else:
            print("It is not an image. Skipping...")
            continue

def threads():
    Thread(name="Submissions", target=submission_thread).start()
        
def main():
    threads()
