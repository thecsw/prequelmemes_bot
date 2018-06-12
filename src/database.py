import sqlite3

def init_database():
    conn = sqlite3.connect("preq.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Submissions (
    post_ID TEXT,
    Quote TEXT DEFAULT "Not Found"
    )""")
    conn.commit()
    c.close()
    conn.close()

def insert(post_ID, Quote="Not Found"):
    conn = sqlite3.connect("preq.db")
    c = conn.cursor()
    c.execute("""INSERT INTO Submissions (
    post_ID,
    Quote) VALUES (?, ?)""", (str(post_ID), Quote))
    conn.commit()
    c.close()
    conn.close()
