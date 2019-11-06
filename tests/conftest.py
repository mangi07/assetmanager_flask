import os
import pytest
import sqlite3
import sys
from unittest.mock import Mock


@pytest.fixture()
def db_conn():
    wd = os.path.dirname(__file__)
    db_path = os.path.join(wd, 'test_db/db.sqlite3')
    db_setup_path = os.path.join(wd, '../db/setup.sql')
    db_teardown_path = os.path.join(wd, '../db/clear_tables.sql')

    conn = sqlite3.connect(db_path)

    with open(db_setup_path) as f:
        script = f.read()
        conn.executescript(script)

    real_sqlite3_connect = sqlite3.connect # save reference to real method
    sqlite3.connect = Mock()
    sqlite3.connect.return_value = real_sqlite3_connect(db_path)
    
    yield conn

    sqlite3.connect = real_sqlite3_connect # recover real method
    with open(db_teardown_path) as f:
        conn = sqlite3.connect(db_path)
        script = f.read()
        conn.executescript(script)
        conn.close()
