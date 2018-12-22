import os

# This is for reddit
CLIENT_ID = os.getenv("BOT_CLIENT_ID")
CLIENT_SECRET = os.getenv("BOT_CLIENT_SECRET")
USERNAME = os.getenv("BOT_USERNAME")
PASSWORD = os.getenv("BOT_PASSWORD")
USER_AGENT = os.getenv("BOT_USER_AGENT")

# Subreddit name
SUBREDDIT = os.getenv("SUBREDDIT")

# Subtitles folder
SUBS_FOLDER = os.getenv("SUBS_FOLDER")

# This is for postgres server
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
