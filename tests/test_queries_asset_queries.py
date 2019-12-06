###############################################################################
# File: test_queries_asset_queries.py
#
###############################################################################

from unittest.mock import Mock
import sqlite3
import pytest

from queries import asset_queries
from queries.query_utils import MyDB


@pytest.fixture
def host():
    asset_queries._get_host_url = Mock()
    asset_queries._get_host_url.return_value = 'host.com/'


@pytest.fixture
def pagination():
    real_pg = asset_queries._get_pagination

    def _inner(page=0, limit=0):
        offset, limit = asset_queries._get_pagination(page, limit)
        asset_queries._get_pagination = Mock(return_value=(offset, limit))
    
    yield _inner
    asset_queries._get_pagination = real_pg


class TestAssetQueries:

    ##########################################################
    # PICTURE LISTINGS FROM ID LIST
    ##########################################################
    def test_get_asset_pictures_1(self, setup_mydb, host):
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
        db = MyDB()
        db._executescript(query)

        pic_groups = asset_queries.get_asset_pictures([1])
        
        assert pic_groups == {1: [f'host.com/img/{img1}', f'host.com/img/{img2}']}, "Expected dict with one key-value pair and correct path to images."
    
    def test_get_asset_pictures_2(self, setup_mydb, host):
        """
        Assumes request.host_url works as expected.

        Given one asset id 1 with no associated pictures,
        should return {1:[]}.
        """

        query = """
            insert into asset (id, asset_id, description) values (1, 'assetone', 'something');
            insert into picture (id, file_path) values (1, 'pic1.jpg'), (2, 'pic2.JPG');
        """
        db = MyDB()
        db._executescript(query)

        pic_groups = asset_queries.get_asset_pictures([1])
        
        assert pic_groups == {1:[]}, "Expected dict with asset id as key to an empty list."
    
    def test_get_asset_pictures_3(self, setup_mydb, host):
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
        db = MyDB()
        db._executescript(query)

        pic_groups = asset_queries.get_asset_pictures([1, 2])
        
        assert pic_groups == {
            1: [f'host.com/img/{img2}'],
            2: [f'host.com/img/{img1}', f'host.com/img/{img2}']
        }, "Expected dict with two key-value pairs and correct paths to images."
    
    def test_get_asset_pictures_4(self, setup_mydb, host):
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
        db = MyDB()
        db._executescript(query)

        pic_groups = asset_queries.get_asset_pictures([1, 2])
        
        assert pic_groups == {
            1: [],
            2: [f'host.com/img/{img1}', f'host.com/img/{img2}']
        }, "Expected dict with two key-value pairs and correct paths to images."


    ##########################################################
    # LOCATION LISTINGS FROM ID LIST
    ##########################################################

    def test_get_asset_locations_1(self):
        """Should return empyt dict given an empty id list"""
        locs_per_id = asset_queries.get_asset_locations([])
        assert locs_per_id == {}

    def test_get_asset_locations_2(self, setup_mydb):
        """Should return dict with key-val pair of id:[] given asset id with no associated locations."""
        query = f"""
            insert into asset (id, asset_id, description) values 
                (1, 'assetone', 'something');
            insert into location (id, description) values (1, 'loc 1');
        """
        db = MyDB()
        db._executescript(query)

        locs_per_id = asset_queries.get_asset_locations([1])
        assert locs_per_id == {1:[]}

    def test_get_asset_locations_3(self, setup_mydb):
        """Should return dict with one key-val pair 
        where key is id and val is dict representing location_count
        when given existing asset id with one location_count."""
        query = f"""
            insert into asset (id, asset_id, description) values 
                (1, 'assetone', 'something');
            insert into location (id, description) values (1, 'loc 1');
            insert into location_count (id, asset, location, count, audit_date) values
                (1, 1, 1, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)

        locs_per_id = asset_queries.get_asset_locations([1])
        assert locs_per_id == {1:[
            {
                'count_id': 1,
                'location_id': 1,
                'description': 'loc 1',
                'parent_id': None,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }
        ]}

    def test_get_asset_locations_4(self, setup_mydb):
        """Given list of 2 ids where first exists and second doesn't,
        should return dict with two key-val pairs 
        where first pair is correct id:location_count
        and second pair is id:[]"""
        query = f"""
            insert into asset (id, asset_id, description) values 
                (1, 'assetone', 'something');
            insert into location (id, description) values (1, 'loc 1');
            insert into location_count (id, asset, location, count, audit_date) values
                (1, 1, 1, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)

        locs_per_id = asset_queries.get_asset_locations([1, 2])
        assert locs_per_id == {
            1:[{
                'count_id': 1,
                'location_id': 1,
                'description': 'loc 1',
                'parent_id': None,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
                }],
            2:[]
        }

    def test_get_asset_locations_5(self, setup_mydb):
        """Given list of 2 existing ids,
        should return dict with two key-val pairs 
        where both pairs have the correct id:location_count"""
        query = f"""
            insert into asset (id, asset_id, description) values 
                (1, 'assetone', 'something'),
                (2, 'assettwo', 'something else');
            insert into location (id, description) values (1, 'loc 1'), (2, 'loc 2');
            insert into location_count (id, asset, location, count, audit_date) values
                (1, 1, 1, 1, '2019-01-01 00:00:00'),
                (2, 2, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)

        locs_per_id = asset_queries.get_asset_locations([1, 2])
        assert locs_per_id == {
            1:[{
                'count_id': 1,
                'location_id': 1,
                'description': 'loc 1',
                'parent_id': None,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
                }],
            2:[{
                'count_id': 2,
                'location_id': 2,
                'description': 'loc 2',
                'parent_id': None,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }]
        }

    def test_get_asset_locations_6(self, setup_mydb):
        """Given list of 1 existing asset id,
        should return dict with one key-val pairs
        where val is a list of 2 dicts,
        each representing a location_count associated with the asset"""
        query = f"""
            insert into asset (id, asset_id, description) values 
                (1, 'assetone', 'something');
            insert into location (id, description) values (1, 'loc 1'), (2, 'loc 2');
            insert into location_count (id, asset, location, count, audit_date) values
                (1, 1, 1, 1, '2019-01-01 00:00:00'),
                (2, 1, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)

        locs_per_id = asset_queries.get_asset_locations([1])
        assert locs_per_id == {
            1:[{
                'count_id': 1,
                'location_id': 1,
                'description': 'loc 1',
                'parent_id': None,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
                },
                {
                'count_id': 2,
                'location_id': 2,
                'description': 'loc 2',
                'parent_id': None,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }]
        }
    

    ##########################################################
    # ASSET LISTINGS QUERY STRING FORMATION
    ##########################################################

    def test__get_asset_query_string_1(self):
        sql = "SELECT asset.id, asset.asset_id, asset.description, asset.cost " \
            "FROM asset LIMIT ?, ?;"
        params = (0, 5)

        fsql, fparams = asset_queries._get_asset_query_string()
        assert fsql == sql
        assert fparams == params

    def test__get_asset_query_string_2(self):
        sql = "SELECT asset.id, asset.asset_id, asset.description, asset.cost " \
            "FROM asset WHERE asset.cost > ? LIMIT ?, ?;"
        params = (100, 0, 5)

        filters = {'asset.cost__gt':100}
        fsql, fparams = asset_queries._get_asset_query_string(filters=filters)
        assert fsql == sql
        assert fparams == params

    
    ##########################################################
    # ASSET LISTINGS
    ##########################################################
    def test_get_assets_1(self, setup_mydb, pagination):
        """Should return [] since there are 0 assets in the database."""
        pagination(page=0, limit=5)
        res = asset_queries.get_assets()
        assert res == {}

    def test_get_assets_2(self, setup_mydb, host, pagination):
        """Should return one asset in asset listing with only one asset in the database."""
        pagination(page=0, limit=5)
        query = f"""
            insert into asset (id, asset_id, description) values 
                (1, '1', 'one');
        """
        db = MyDB()
        db._executescript(query)
        res = asset_queries.get_assets()
        assert len(res) == 1

    def test_get_assets_3(self, setup_mydb, host, pagination):
        """Should return two assets in asset listing with only two assets in the database."""
        pagination(page=0, limit=5)
        query = f"""
            insert into asset (id, asset_id, description, cost) values 
                (1, '1', 'one', 100), (2, '2', 'two', 350.50);
        """
        db = MyDB()
        db._executescript(query)
        res = asset_queries.get_assets()
        assert len(res) == 2
    
    def test_get_assets_4(self, setup_mydb, host, pagination):
        """Should return asset with correct empty data structures."""
        pagination(page=0, limit=5)
        query = f"""
            insert into asset (id, asset_id, description) values 
                (1, '1', 'one'), (2, '2', 'two');
        """
        db = MyDB()
        db._executescript(query)
        res = asset_queries.get_assets()
        assert res[1]['location_counts'] == []
        assert res[1]['pictures'] == []
        assert res[1]['invoices'] == []
        assert res[1]['far'] == {}

    
    ##########################################################
    # ASSET PAGINATION
    ##########################################################
    @pytest.mark.parametrize("page, limit, count", [
        (0, 5, 5), (0, 4, 4), (0, 6, 6), (1, 4, 2), (1, 5, 1), (1, 6, 0)
    ])
    def test_get_assets_pagination_1(self, setup_mydb, host, pagination, page, limit, count):
        """Should return the correct number of assets given pagination arguments."""
        query = f"""
            insert into asset (id, asset_id, description) values 
                (1, '1', 'one'), (2, '2', 'two'), (3, '3', 'three'),
                (4, '4', 'four'), (5, '5', 'five'), (6, '6', 'six');
        """
        pagination(page, limit)
        db = MyDB()
        db._executescript(query)
        res = asset_queries.get_assets()
        assert len(res) == count

    
    ##########################################################
    # TODO: ASSET FILTERING
    ##########################################################


    ##########################################################
    # TODO: ASSET FILTERING WITH PAGINATION
    ##########################################################

    def blah():
        assert res == {
            1:{
                'id':1, 
                'asset_id':'1', 
                'description':'one', 
                'cost':100,
                'location_counts':[],
                'pictures':[],
                'invoices':[],
                'far':{}
            },
            2:{
                'id':2, 
                'asset_id':'2', 
                'description':'two', 
                'cost':350.50,
                'location_counts':[],
                'pictures':[],
                'invoices':[],
                'far':{}
            }
        }

    
