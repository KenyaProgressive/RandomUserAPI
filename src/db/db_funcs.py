import sqlite3


def create_db():
    conn = sqlite3.connect("random_user.db")
    return conn


def make_table_random_user(curr: sqlite3.Cursor):
    try:
        curr.execute("CREATE TABLE random_user(Sex BOOLEAN NOT NULL CHECK (Sex in (0, 1)),"
                     "Name VARCHAR(100),"
                     "Surname VARCHAR(150),"
                     "Phone_number VARCHAR(15),"
                     "Email VARCHAR(150),"
                     "residental_address TEXT,"
                     "photo BLOB)")
    except Exception as exception:
        print(exception)
