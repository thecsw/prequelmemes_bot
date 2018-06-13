import sqlite3

# If preq.db doesn't exist, creates a new file
def init_database():
    conn = sqlite3.connect("preq.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS Submissions (
    post_ID TEXT,
    Quote TEXT DEFAULT "Not Found"
    );
    """)
    conn.commit()
    c.close()
    conn.close()

# Inserts a new row with post_ID = post_ID
# and Quote = "Not Found"
def insert(post_ID):
    conn = sqlite3.connect("preq.db")
    c = conn.cursor()
    c.execute("""
    INSERT INTO Submissions (
    post_ID
    ) 
    VALUES (?);
    """, (str(post_ID), ))
    conn.commit()
    c.close()
    conn.close()

# Inserts a quote instead of "Not Found"
def update_post(post_ID, quote):
    conn = sqlite3.connect("preq.db")
    c = conn.cursor()
    c.execute("""
    UPDATE Submissions
    SET Quote = ? 
    WHERE post_ID = ?;
    """, (quote, str(post_ID), ))
    conn.commit()
    c.close()
    conn.close()

# Returns an array of 100 last checked submissions
def get_latest():
    conn = sqlite3.connect("preq.db")
    c = conn.cursor()
    args = c.execute("""
    SELECT post_ID FROM Submissions ORDER BY post_ID DESC LIMIT 100;
    """)
    result = args.fetchall()
    conn.commit()
    c.close()
    conn.close()
    return [x[0] for x in result]

def get_done():
    conn = sqlite3.connect("preq.db")
    c = conn.cursor()
    args = c.execute("""
    SELECT * FROM Submissions 
    WHERE rowid = (SELECT MAX(rowid) FROM Submissions);
    """)
    result = list(args.fetchone())
    conn.commit()
    c.close()
    conn.close()
    return result
