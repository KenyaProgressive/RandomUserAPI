import sqlite3
from typing import List



def make_db(curr: sqlite3.Cursor, table_name: str, table_fields: List[str]):
    try:
        curr.execute("CREATE TABLE ? (?)", table_name, table_fields)
    except Exception as e:
        print(e)
