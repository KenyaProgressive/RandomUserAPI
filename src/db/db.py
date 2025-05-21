import sqlite3
from db_funcs import *
from src.const import USERS_DATA_FIELDS

conn = sqlite3.connect("random_user.db")
cursor = conn.cursor()

make_db(conn, "UsersData", USERS_DATA_FIELDS)


