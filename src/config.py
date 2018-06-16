import os

# This is for reddit
client_id = os.getenv("BOT_CLIENT_ID")
client_secret = os.getenv("BOT_CLIENT_SECRET")
username = os.getenv("BOT_USERNAME")
password = os.getenv("BOT_PASSWORD")
user_agent = os.getenv("BOT_USER_AGENT")

# Subreddit name
subreddit = os.getenv("SUBREDDIT")

# This is for postgres server
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_user = os.getenv("POSTGRES_USER")
db_pass = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
