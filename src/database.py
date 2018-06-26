import psycopg2

# If preq.db doesn't exist, creates a new file
def init_database(conn):
    c = conn.cursor()
    sql_query = """
    CREATE TABLE IF NOT EXISTS Submissions (
    rowid SERIAL PRIMARY KEY,
    post_ID TEXT,
    Quote TEXT DEFAULT 'Not Found');"""
    c.execute(sql_query)
    conn.commit()
    c.close()

def add_record(conn, post_ID, Quote="Not Found"):
    c = conn.cursor()
    sql_query = """
    INSERT INTO Submissions (post_ID, Quote)
    VALUES (%s, %s);"""
    c.execute(sql_query, (post_ID, Quote,))
    conn.commit()
    c.close()

def count_quote(conn, Quote):
    c = conn.cursor()
    sql_query  = """
    SELECT COUNT(1) FROM Submissions WHERE Quote = %s;"""
    c.execute(sql_query, (Quote,))
    res = c.fetchall()[0][0]
    c.close()
    return res

def get_latest(conn):
    c = conn.cursor()
    sql_query = """
    SELECT post_ID FROM Submissions ORDER BY rowid DESC LIMIT 100;"""
    c.execute(sql_query)
    res = c.fetchall()
    res = [x[0] for x in res]
    c.close()
    return res

def get_done(conn):
    c = conn.cursor()
    sql_query = """
    SELECT Quote FROM Submissions ORDER BY rowid DESC LIMIT 1;"""
    c.execute(sql_query)
    res = c.fetchall()[0]
    c.close()
    return res
