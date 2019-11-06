###############################################################################
# File: test_queries_asset_queries.py
#
###############################################################################

from queries import asset_queries
from unittest.mock import Mock
import sqlite3
import pytest


@pytest.fixture
def host():
    asset_queries._get_host_url = Mock()
    asset_queries._get_host_url.return_value = 'host.com/'

class TestAssetQueries:

    def test_get_asset_pictures_1(self, db_conn, host):
        """
        Assumes request.host_url works as expected.

        Given asset with id 1 and 2 associated pics,
        should return dict with 1 key/val pair:
            key: given id
            value: list of 2 correct img paths
        """
        
        img1 = '1.jpg'
        img2 = '2.JPG'
        query = f"""
            insert into asset (id, asset_id, description) values (1, 'assetone', 'something');
            insert into picture (id, file_path) values (1, '{img1}'), (2, '{img2}');
            insert into asset_picture (asset, picture) values (1, 1), (1, 2);
        """
        db_conn.executescript(query)
        db_conn.close()

        pic_groups = asset_queries.get_asset_pictures([1])
        
        assert pic_groups == {1: [f'host.com/img/{img1}', f'host.com/img/{img2}']}, "Expected dict with one key-value pair and correct path to images."
    
    def test_get_asset_pictures_2(self, db_conn, host):
        """
        Assumes request.host_url works as expected.

        Given one asset id 1 with no associated pictures,
        should return {1:[]}.
        """

        query = """
            insert into asset (id, asset_id, description) values (1, 'assetone', 'something');
            insert into picture (id, file_path) values (1, 'pic1.jpg'), (2, 'pic2.JPG');
        """
        db_conn.executescript(query)
        db_conn.close()

        pic_groups = asset_queries.get_asset_pictures([1])
        
        assert pic_groups == {1:[]}, "Expected dict with asset id as key to an empty list."
    
    def test_get_asset_pictures_3(self, db_conn, host):
        """
        Assumes request.host_url works as expected.

        Given 2 assets that both have associated pics,
        should return dict with 2 key/val pairs:
            key: given id
            value: list of correct img path(s)
        """
        
        img1 = '1.jpg'
        img2 = '2.JPG'
        query = f"""
            insert into asset (id, asset_id, description) values 
                (1, 'assetone', 'something'),
                (2, 'assettwo', 'something 2');
            insert into picture (id, file_path) values (1, '{img1}'), (2, '{img2}');
            insert into asset_picture (asset, picture) values (1,2), (2, 1), (2, 2);
        """
        db_conn.executescript(query)
        db_conn.close()

        pic_groups = asset_queries.get_asset_pictures([1, 2])
        
        assert pic_groups == {
            1: [f'host.com/img/{img2}'],
            2: [f'host.com/img/{img1}', f'host.com/img/{img2}']
        }, "Expected dict with two key-value pairs and correct paths to images."
    
    def test_get_asset_pictures_4(self, db_conn, host):
        """
        Assumes request.host_url works as expected.

        Given 2 assets where only one has associated pics,
        should return dict with 2 key/val pairs.
        """
        
        img1 = '1.jpg'
        img2 = '2.JPG'
        query = f"""
            insert into asset (id, asset_id, description) values 
                (1, 'assetone', 'something'),
                (2, 'assettwo', 'something 2');
            insert into picture (id, file_path) values (1, '{img1}'), (2, '{img2}');
            insert into asset_picture (asset, picture) values (2, 1), (2, 2);
        """
        db_conn.executescript(query)
        db_conn.close()

        pic_groups = asset_queries.get_asset_pictures([1, 2])
        
        assert pic_groups == {
            1: [],
            2: [f'host.com/img/{img1}', f'host.com/img/{img2}']
        }, "Expected dict with two key-value pairs and correct paths to images."
    