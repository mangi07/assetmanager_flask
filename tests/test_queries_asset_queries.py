###############################################################################
# File: test_queries_asset_queries.py
#
###############################################################################

from queries import asset_queries
from unittest.mock import Mock
import sqlite3
import pytest

class DB:
    __instance = None

    def execute_script(self, sql_file):
        cur = self.con.cursor()
        f = open(sql_file)
        script = f.read()
        cur.executescript(script)
        cur.close()
    
    def connection(self):
        return self.con

    def clear(self):
        self.execute_script("../db/clear_tables.sql")

    @staticmethod 
    def getInstance():
        if DB.__instance == None:
            DB.__instance = DB()
        return DB.__instance

    def __init__(self):
        if DB.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.con = sqlite3.connect(":memory:")
            self.execute_script("../db.setup.sql")
            DB.__instance = self


@pytest.fixture
def db():
    asset_queries._get_host_url = Mock()
    asset_queries._get_host_url.return_value = 'host.com'

    db = DB.getInstance()
    yield db
    db.clear()

class TestAssetQueries:

    def test_get_asset_pictures_(self, db):
        """
        Assumes request.host_url works as expected.
        Should return dict with 1 key/val pair:
            key: given id
            value: list of 2 correct img paths"""
        asset_queries._get_host_url = Mock()
        asset_queries._get_host_url.return_value = 'host.com'
        # TODO: need to mock here to use db fixture with in-memory database
        pic_groups = asset_queries.get_asset_pictures([1])
        
        assert False, "Expected {id: ['host.com/img/pic1', 'host.com/img/pic2']}"
    
    def test_two(self, db):
        pass
