from db_funcs import *
from src.api.api import get_users_info, parse_result
import os

cursor = create_db()

if not os.path.exists("random_user.db"):
    make_table_random_user(cursor)

a = get_users_info().json()
print(a)





