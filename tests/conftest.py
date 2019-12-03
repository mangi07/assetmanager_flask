import os
import pytest
import sqlite3
import sys
from unittest.mock import Mock

from queries.query_utils import MyDB

@pytest.fixture()
def setup_mydb():
    wd = os.path.dirname(__file__)
    db_path = os.path.join(wd, 'test_db/db.sqlite3')
    db_setup_path = os.path.join(wd, '../db/setup.sql')
    db_teardown_path = os.path.join(wd, '../db/clear_tables.sql')

    real_sqlite3_connect = sqlite3.connect # save reference to real method
    sqlite3.connect = Mock(side_effect = lambda path : real_sqlite3_connect(db_path) )
    #sqlite3.connect.return_value = real_sqlite3_connect(db_path)

    db = MyDB()

    with open(db_setup_path) as f:
        script = f.read()
        db._executescript(script)
    
    yield db_path

    with open(db_teardown_path) as f:
        db = MyDB() # may need to reconnect to db in case of errors while testing
        script = f.read()
        db._executescript(script)

    sqlite3.connect = real_sqlite3_connect # recover real method
