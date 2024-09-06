import os

from dotenv import load_dotenv


load_dotenv()


def get_db_path():
    #return "./db/db.sqlite3"
    return os.getenv('DB_PATH')

DB_PATH = get_db_path()
assert type(DB_PATH) == str
