import sqlite3
from contextlib import contextmanager


@contextmanager
def db_connection(path):
    conn = sqlite3.connect(path)
    try:
        yield conn.cursor()
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


with db_connection("mydb.db") as c:
    c.execute("CREATE TABLE IF NOT EXISTS person (name VARCHAR(255), age INT);")

with db_connection("mydb.db") as c:
    c.execute("INSERT INTO person VALUES ('Redd', 25)")

try:
    with db_connection("mydb.db") as c:
        c.execute("INSERT INTO person VALUES ('Ghost', 99)")
        raise ValueError("oops")
except ValueError:
    pass

with db_connection("mydb.db") as c:
    c.execute("SELECT * FROM person")
    print(c.fetchall())