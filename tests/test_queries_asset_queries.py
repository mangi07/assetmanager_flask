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
        #cur = self.con.cursor()
        f = open(sql_file)
        script = f.read()
        self.cur.executescript(script)
        #cur.close()
    
    def connection(self):
        return self.con

#    def clear(self):
#        if self.con is not None:
#            #cur = self.con.cursor
#            self.execute_script("./db/clear_tables.sql")
#            self.cur.close()

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
            self.cur = self.con.cursor()
            self.execute_script("./db/setup.sql")
            DB.__instance = self


@pytest.fixture
def db():
    asset_queries._get_host_url = Mock()
    asset_queries._get_host_url.return_value = 'host.com'

    db = DB.getInstance()
    sqlite3.connect = Mock()
    sqlite3.connect.return_value = db.connection()
    yield db
    #db.clear()


class TestAssetQueries:

    def test_get_asset_pictures_1(self, db):
        """
        Assumes request.host_url works as expected.
        Should return dict with 1 key/val pair:
            key: given id
            value: list of 2 correct img paths"""
        asset_queries._get_host_url = Mock()
        asset_queries._get_host_url.return_value = 'host.com/'
        
        # TODO: need to mock here to use db fixture with in-memory database
        cur = db.connection().cursor()
        query = """
            insert into asset (id, asset_id, description) values (1, 'assetone', 'something');
            insert into picture (id, file_path) values (1, 'pic1.jpg'), (2, 'pic2.JPG');
            insert into asset_picture (asset, picture) values (1, 1), (1, 2);
        """
        cur.executescript(query)

        pic_groups = asset_queries.get_asset_pictures([1])
        
        assert pic_groups == {1: ['host.com/img/pic1.jpg', 'host.com/img/pic2.JPG']}, "Expected {id: ['host.com/img/pic1.jpg', 'host.com/img/pic2.JPG']}"
    
    def test_two(self, db):
        pass
