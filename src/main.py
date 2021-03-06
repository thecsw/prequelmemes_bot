"""                              _                          
 _ __  _ __ ___  __ _ _   _  ___| |_ __ ___   ___ _ __ ___   ___  ___
| '_ \| '__/ _ \/ _` | | | |/ _ \ | '_ ` _ \ / _ \ '_ ` _ \ / _ \/ __|
| |_) | | |  __/ (_| | |_| |  __/ | | | | | |  __/ | | | | |  __/\__ \
| .__/|_|  \___|\__, |\__,_|\___|_|_| |_| |_|\___|_| |_| |_|\___||___/
|_|                |_|                                      

"""
# All the necessary imports

import time
from threading import Thread
import re
import glob
import logging

# Separate pip modules/packages

import psycopg2
import praw
import pysrt

# Our own scripts

import message
import text_recognition
import banlist
import signal_handler
import database
import config

REDDIT = praw.Reddit(client_id=config.CLIENT_ID,
                     client_secret=config.CLIENT_SECRET,
                     username=config.USERNAME,
                     password=config.PASSWORD,
                     user_agent=config.USER_AGENT)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

SUBREDDIT = REDDIT.subreddit(config.SUBREDDIT)

# subreddit = reddit.subreddit('pewds_test')
# If you want to test it out, go to r/pewds_test
# I created this subreddit just for personal testings
# Feel free to use it

SUBS_DIR = "./subtitles/"

def add_zero(string):
    """
    Adds 0 in front of a digit
    """
    if len(string) == 1:
        string = f"0{string}"

    return string

def riptime(subrip_time):
    """
    Formats time
    """
    hours = add_zero(str(subrip_time.hours))
    minutes = add_zero(str(subrip_time.minutes))
    seconds = add_zero(str(subrip_time.seconds))
    time_string = f"{hours}:{minutes}:{seconds}"

    return time_string

def reply_post(post, msg):
    """
    Replies to a post
    """
    try:
        reply = post.reply(msg)
        logging.info(f"Reply sent! ID - {reply}")
    except Exception as e:
        logging.error(f"Error replying. {e}")
    time.sleep(10)

def replace_chars(text):
    """
    Well, this is obvious,
    clears some non-ASCII characters
    """
    text = re.sub('[^a-zA-Z0-9\n]+', '', text)
    return text

def parse_url(post):
    """
    Catches all media files that OCR can work with
    """
    pattern = re.compile(r".(jpe?g|png|gifv?)(\?\S*)?")
    if pattern.search(post.url) is not None:
        return True
    return False

def show_out(conn):
    """
    Searches history
    """
    latest = database.get_done(conn)
    logging.info(f"Found Citation : {latest[0]}")

def validate_text(post):
    """
    This function is used to extract text from a post's image, filter it
    and return a list of found and acceptable strings. If any error has
    occured or the final list after filtering is empty, the function will
    return False. If it returned False, no quote can be found.
    """

    # Checks if it is possible to find text, if not, return False
    if parse_url(post):
        try:
            image_extracted = text_recognition.extract_image(post)
            logging.info(f"Filesize -> {text_recognition.check_size('temp')/1000}KB")
            if not image_extracted:
                logging.error(f"Filesize exceeded 10MB.")
                return False

            recog_text = text_recognition.text_recognition(image_extracted).decode("utf-8").lower()
        except Exception as e:
            logging.error(f"Error occured. {e}")
            return False
    else:
        logging.error("Image not found.")
        return False

    # Some text filterting.
    formatted_text = (replace_chars(recog_text).lower().split())[::-1]
    formatted_text = [i for i in formatted_text if len(i) > 8 and not i in banlist.banlist]

    # If the list is empty, no need for scanning
    if not formatted_text:
        logging.error("No text found.")
        return False

    return formatted_text

def search_quote(conn, formatted_text, post):
    """
    This function receives a list of strings and tries to find them
    in files from subtitles folder. On the first occurence, it will
    reply to submissions and return found citation. If no citation
    found, the function just returns False.
    """

    for filename in glob.glob(SUBS_DIR + "*.srt"):

        subs = pysrt.open(filename)

        for found_word in formatted_text:
            for quote in subs:
                quote_text = replace_chars(quote.text).lower()
                quote_text = quote_text.replace("\n", "")

                # The reverse text memes are quite popular now.
                # We can easily spot even the inverse quotes.
                if (found_word in quote_text) or (found_word[::-1] in quote_text):
                    citation = quote.text.replace("\n", " ")
                    movie = filename.replace("_", " ").replace(".srt", "").replace(SUBS_DIR, "")
                    start = riptime(quote.start)
                    end = riptime(quote.end)

                    referenced_times = database.count_quote(conn, citation)

                    reply_message = message.modify_message(citation, movie, start,
                                                           end, referenced_times)
                    reply_post(post, reply_message)
                    return citation
    return False

def submission_thread():
    """
    This is the main submission thread, it listens to all
    new submissions in a subreddit, returns a post instance,
    extract image and text, fills out the database. If SIGINT
    or SIGTERM is received, the database connection will be
    closed and the program will be gracefully killed.
    """

    logging.warning("Sleeping for 10 seconds. Waiting for the database to turn on...")
    time.sleep(10)

    killer = signal_handler.GracefulKiller

    conn = psycopg2.connect(dbname=config.DB_NAME,
                            user=config.DB_USER,
                            password=config.DB_PASS,
                            host=config.DB_HOST,
                            port=config.DB_PORT)

    database.init_database(conn)

    for submission in SUBREDDIT.stream.submissions():
        post = REDDIT.submission(submission)
        post_id = str(post.id)
        logging.info("")
        logging.info("------------------------")
        logging.info(f"Starting new submission. {post_id}")
        latest_posts = database.get_latest(conn)

        # If the post has been processed recently,
        # skip it then
        if post_id in latest_posts:
            logging.info("The post already has been evaluated.")
            continue

        formatted_text = validate_text(post)
        if not formatted_text:
            database.add_record(conn, post_id)
            continue

        citation = search_quote(conn, formatted_text, post)
        if not citation:
            database.add_record(conn, post_id)
            logging.info("Citation is not found.")
            continue

        database.add_record(conn, post_id, citation)
        logging.info("Record has been added to the database.")
        show_out(conn)
        safe_kill(killer, conn)

def save_karma():
    """
    This function "saves us karma". This means that every 30 minutes, this
    function will loop through our last 100 comments and upvote threshold them.
    If any comment has more than 2 downvotes, so the overall score is -2, the
    comment gets auto-deleted. This is a nice function that can save us some
    points and karma because sometimes the bot can be false positive.
    """

    memepolice = REDDIT.redditor(config.USERNAME)
    while True:
        for comment in memepolice.comments.new(limit=100):
            # It will parse 100 comments in 5-6 seconds
            if comment.ups < -2:
                comment.delete()

        time.sleep(1800)

def safe_kill(killer, conn):
    """
    Gracefully killing.
    """

    # If SIGINT or SIGTERM received, exit.
    if killer.kill_now:
        logging.warning("Committing and shutting down the database connection.")
        conn.commit()
        conn.close()
        logging.warning("Closed.")
        exit("Received a termination signal. Bailing out.")


def threads():
    """
    This function just starts main threads, one to parse submissions,
    second to save karma.
    """

    Thread(name="Submissions", target=submission_thread).start()
    Thread(name="Save Karma", target=save_karma).start()

if __name__ == "__main__":
    threads()
