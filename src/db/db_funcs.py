import sqlite3
from src.api.api import get_users_info, parse_result, get_photo_from_disk
import shutil

def create_db(path_to_db: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path_to_db, check_same_thread=False)
    return conn


def make_table_random_user(curr: sqlite3.Cursor) -> None:
    try:
        curr.execute("CREATE TABLE if not exists random_user(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "Sex VARCHAR(6) NOT NULL CHECK (Sex in ('male', 'female')),"
                     "Name VARCHAR(100),"
                     "Surname VARCHAR(150),"
                     "Phone_number VARCHAR(15),"
                     "Email VARCHAR(150),"
                     "residental_address TEXT,"
                     "photo BLOB)")
    except Exception as exception:
        print(exception)


def push_data_to_table(curr: sqlite3.Cursor, conn: sqlite3.Connection):
    users_data_json = get_users_info()
    parsed_data = parse_result(users_data_json)
    values_to_push = prepare_data_for_push(parsed_data)
    query = """INSERT INTO random_user(Sex, Name, Surname, Phone_number, Email, residental_address, photo) VALUES (?, ?, ?, ?, ?, ?, ?)"""
    try:
        curr.executemany(query, values_to_push)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        shutil.rmtree("photos")
    return parsed_data


def prepare_data_for_push(parsed_data: list):
    prepared = []
    for data in parsed_data:
        temp = (
            data['gender'],
            data['name'],
            data['surname'],
            data['phone_number'],
            data['email'],
            data['residental_address']
        )
        photo_to_push = get_photo_from_disk(f"photos/{data['photo']}")
        result = (*temp, photo_to_push)
        prepared.append(result)
    return prepared

def get_users_info_from_db(curr: sqlite3.Cursor, limit: int):
    result = curr.execute("SELECT * FROM random_user")
    return result.fetchmany(limit)

def get_users_count(curr: sqlite3.Cursor):
    result = curr.execute("SELECT COUNT(*) FROM random_user")
    return result.fetchone()[0]
