###############################################################################
# File: test_queries_asset_queries.py
#
###############################################################################

from unittest.mock import Mock
import sqlite3
import pytest

import config
from queries import asset_queries
from queries.query_utils import MyDB


@pytest.fixture
def host():
    asset_queries._get_host_url = Mock()
    asset_queries._get_host_url.return_value = 'host.com/'


@pytest.fixture
def pagination():
    real_pg = asset_queries._get_pagination

    def _inner(page, limit):
        offset = page * limit
        asset_queries._get_pagination = Mock(return_value=(offset, limit))
    
    yield _inner
    asset_queries._get_pagination = real_pg


@pytest.fixture
def page_limit():
    real_limit = config.get_pagination_limit

    def _inner(limit):
        config.get_pagination_limit = Mock(return_value=(limit))
    
    yield _inner
    config.get_pagination_limit = real_limit


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
    # LOCATION LISTINGS FROM ID LIST TODO: might not use this
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
    # TODO: LOCATION LISTINGS FROM FILTERS
    ##########################################################
    
    def test_get_locations_from_filters_1(self, setup_mydb):
        """Should return all records in location_count, since there are no filters."""
        query = """
        insert into location_count (id, asset, location, count, audit_date) values
            (1, 1, 1, 1, '2019-01-01 00:00:00'),
            (2, 1, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)
        location_counts = asset_queries.get_location_counts()
        assert location_counts == {
            1:[{
                'location_id': 1,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
                },
                {
                'location_id': 2,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }]
        }

    def test_get_locations_from_filters_2(self, setup_mydb):
        """Should return all records in location_count without error,
        given filters where none are relevant to location filtering."""
        query = """
        insert into location_count (id, asset, location, count, audit_date) values
            (1, 1, 1, 1, '2019-01-01 00:00:00'),
            (2, 1, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)
        location_counts = asset_queries.get_location_counts(filters={'asset.id__includes':[999]})
        assert location_counts == {
            1:[{
                'location_id': 1,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
                },
                {
                'location_id': 2,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }]
        }

    def test_get_locations_from_filters_3(self, setup_mydb):
        """Should return all records in location_count without error,
        given filters where some are relevant to location filtering and some aren't."""
        query = """
        insert into location_count (id, asset, location, count, audit_date) values
            (1, 1, 1, 1, '2019-01-01 00:00:00'),
            (2, 1, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)
        location_counts = asset_queries.get_location_counts(
            filters={
                'asset.id__includes':[999],
                'location_count.id__eq':2
            }
        )
        assert location_counts == {
            1:[
                {
                'location_id': 2,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }]
        }

    def test_get_locations_from_filters_4(self, setup_mydb):
        """Should return all records in location_count without error,
        given filters where all are relevant to location filtering."""
        query = """
        insert into location_count (id, asset, location, count, audit_date) values
            (1, 1, 1, 1, '2019-01-01 00:00:00'),
            (2, 1, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)
        location_counts = asset_queries.get_location_counts(
            filters={
                'location_count.id__eq':2
            }
        )
        assert location_counts == {
            1:[
                {
                'location_id': 2,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }]
        }

    def test_get_locations_from_filters_5(self, setup_mydb):
        """Should return all records in location_count without error,
        given all records' audit_dates are past audit_date__gt filter."""
        query = """
        insert into location_count (id, asset, location, count, audit_date) values
            (1, 1, 1, 1, '2019-01-01 00:00:00'),
            (2, 1, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)
        location_counts = asset_queries.get_location_counts(
            filters={
                'location_count.audit_date__gt':'2018-12-31 23:59:59'
            }
        )
        assert location_counts == {
            1:[{
                'location_id': 1,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
                },
                {
                'location_id': 2,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }]
        }
    
    def test_get_locations_from_filters_6(self, setup_mydb):
        """Should return all records in location_count without error,
        given all records' audit_dates are before audit_date__lt filter."""
        query = """
        insert into location_count (id, asset, location, count, audit_date) values
            (1, 1, 1, 1, '2019-01-01 00:00:00'),
            (2, 1, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)
        location_counts = asset_queries.get_location_counts(
            filters={
                'location_count.audit_date__lt':'2019-01-01 00:00:01'
            }
        )
        assert location_counts == {
            1:[{
                'location_id': 1,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
                },
                {
                'location_id': 2,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }]
        }
    
    def test_get_locations_from_filters_7(self, setup_mydb):
        """Should not return any records, given all records' audit_dates are 
        before audit_date__gt filter."""
        query = """
        insert into location_count (id, asset, location, count, audit_date) values
            (1, 1, 1, 1, '2019-01-01 00:00:00'),
            (2, 1, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)
        location_counts = asset_queries.get_location_counts(
            filters={
                'location_count.audit_date__gt':'2019-01-01 00:00:01'
            }
        )
        assert location_counts == {}

    def test_get_locations_from_filters_8(self, setup_mydb):
        """Should not return any records, given all of the records' audit_dates are 
        after audit_date__lt filter."""
        query = """
        insert into location_count (id, asset, location, count, audit_date) values
            (1, 1, 1, 1, '2019-01-01 00:00:00'),
            (2, 1, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)
        location_counts = asset_queries.get_location_counts(
            filters={
                'location_count.audit_date__lt':'2018-12-31 23:59:59'
            }
        )
        assert location_counts == {}
    
    def test_get_locations_from_filters_9(self, setup_mydb):
        """Should return both records since they are both within the date range."""
        query = """
        insert into location_count (id, asset, location, count, audit_date) values
            (1, 1, 1, 1, '2019-02-01 00:00:00'),
            (2, 1, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)
        location_counts = asset_queries.get_location_counts(
            filters={
                'location_count.audit_date__gt':'2018-12-31 23:59:59',
                'location_count.audit_date__lt':'2019-02-01 00:00:01'
            }
        )
        assert location_counts == {
            1:[{
                'location_id': 1,
                'count': 1,
                'audit_date': '2019-02-01 00:00:00'
                },
                {
                'location_id': 2,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }]
        }

    def test_get_locations_from_filters_10(self, setup_mydb):
        """Should not return either record, since neither are within the date range."""
        query = """
        insert into location_count (id, asset, location, count, audit_date) values
            (1, 1, 1, 1, '2019-02-01 00:00:00'),
            (2, 1, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)
        location_counts = asset_queries.get_location_counts(
            filters={
                'location_count.audit_date__gt':'2019-02-01 00:00:01',
                'location_count.audit_date__lt':'2020-01-01 00:00:00'
            }
        )
        assert location_counts == {}
    
    def test_get_locations_from_filters_11(self, setup_mydb):
        """Should only return the record that is within the date range."""
        query = """
        insert into location_count (id, asset, location, count, audit_date) values
            (1, 1, 1, 1, '2019-02-01 00:00:00'),
            (2, 1, 2, 1, '2019-01-01 00:00:00');
        """
        db = MyDB()
        db._executescript(query)
        location_counts = asset_queries.get_location_counts(
            filters={
                'location_count.audit_date__gt':'2018-12-31 24:59:59',
                'location_count.audit_date__lt':'2019-02-01 00:00:00'
            }
        )
        assert location_counts == {
            1:[{
                'location_id': 2,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }]
        }

    def test_get_locations_from_filters_12(self, setup_mydb):
        """Should only return the records that are within the date range
        and match the location filters."""
        query = """
        insert into location_count (id, asset, location, count, audit_date) values
            (1, 1, 1, 1, '2019-01-01 00:00:00'),
            (2, 2, 2, 1, '2019-01-01 00:00:00'),
            (3, 3, 2, 1, '2024-01-01 00:00:00'),
            (4, 4, 3, 1, '2019-01-01 00:00:00'),
            (5, 5, 2, 1, '2020-01-01 00:00:00')
            ;
        """
        db = MyDB()
        db._executescript(query)
        location_counts = asset_queries.get_location_counts(
            filters={
                'location_count.audit_date__gt':'2018-01-01 00:00:00',
                'location_count.audit_date__lt':'2021-01-01 00:00:00',
                'location_count.location__includes':[2, 3]
            }
        )
        assert location_counts == {
            2:[{
                'location_id': 2,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }],
            4:[{
                'location_id': 3,
                'count': 1,
                'audit_date': '2019-01-01 00:00:00'
            }],
            5:[{
                'location_id': 2,
                'count': 1,
                'audit_date': '2020-01-01 00:00:00'
            }],
        }

    ##########################################################
    # ASSET LISTINGS QUERY STRING FORMATION
    ##########################################################

    def test__get_asset_query_string_1(self, page_limit):
        sql = "SELECT asset.id, asset.asset_id, asset.description, asset.cost " \
            "FROM asset LIMIT ?, ?;"
        limit = 5
        page_limit(limit)
        params = (0, limit)

        fsql, fparams = asset_queries._get_asset_query_string()
        assert fsql == sql
        assert fparams == params

    def test__get_asset_query_string_2(self, page_limit, setup_mydb):
        sql = "SELECT asset.id, asset.asset_id, asset.description, asset.cost " \
            "FROM asset WHERE asset.cost > ? LIMIT ?, ?;"
        limit = 5
        page_limit(limit)
        params = (100, 0, limit)

        filters = {'asset.cost__gt':100}
        fsql, fparams = asset_queries._get_asset_query_string(filters=filters)
        assert fsql == sql
        assert fparams == params

    
    ##########################################################
    # ASSET LISTINGS
    ##########################################################
    def test_get_assets_1(self, setup_mydb, pagination):
        """Should return {} since there are 0 assets in the database."""
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
        assert res[1]['location_counts'] == {}
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


    @pytest.mark.parametrize("page, offset, limit", [
        (0, 0, 4), (1, 4, 4), (2, 8, 4), (2, 50, 25)
    ])
    def test__get_pagination(self, page_limit, page, offset, limit):
        """Should return the correct (offset, limit) tuple."""
        page_limit(limit)
        O, L = asset_queries._get_pagination(page)
        assert (O, L) == (offset, limit)

    
    ##########################################################
    # ASSET FILTERING
    ##########################################################
    @pytest.mark.parametrize("gt, count", [
        (99, 6), (100, 5), (299, 4), (300, 3), (600, 0), 
    ])
    def test_get_assets_filtering_1(self, setup_mydb, host, pagination, gt, count):
        """Should return the correct number of assets given gt filter on cost."""
        query = f"""
            insert into asset (id, asset_id, description, cost) values 
                (1, '1', 'one', 100), (2, '2', 'two', 200), (3, '3', 'three', 300),
                (4, '4', 'four', 400), (5, '5', 'five', 500), (6, '6', 'six', 600);
        """
        pagination(page=0, limit=6)
        db = MyDB()
        db._executescript(query)
        filters = {'asset.cost__gt':gt}
        res = asset_queries.get_assets(filters=filters)
        assert len(res) == count
    

    @pytest.mark.parametrize("lt, count", [
        (100, 0), (101, 1), (300, 2), (301, 3), (600, 5), (601, 6),
    ])
    def test_get_assets_filtering_2(self, setup_mydb, host, pagination, lt, count):
        """Should return the correct number of assets given lt filter on cost."""
        query = f"""
            insert into asset (id, asset_id, description, cost) values 
                (1, '1', 'one', 100), (2, '2', 'two', 200), (3, '3', 'three', 300),
                (4, '4', 'four', 400), (5, '5', 'five', 500), (6, '6', 'six', 600);
        """
        pagination(page=0, limit=6)
        db = MyDB()
        db._executescript(query)
        filters = {'asset.cost__lt':lt}
        res = asset_queries.get_assets(filters=filters)
        assert len(res) == count


    @pytest.mark.parametrize("gt, lt, count", [
        (99, 601, 6), (100, 601, 5), (100, 600, 4), 
        (399, 400, 0), (399, 401, 1), 
        (600, 100, 0), (599, 100, 0),
    ])
    def test_get_assets_filtering_3(self, setup_mydb, host, pagination, gt, lt, count):
        """Should return the correct number of assets given cost range."""
        query = f"""
            insert into asset (id, asset_id, description, cost) values 
                (1, '1', 'one', 100), (2, '2', 'two', 200), (3, '3', 'three', 300),
                (4, '4', 'four', 400), (5, '5', 'five', 500), (6, '6', 'six', 600);
        """
        pagination(page=0, limit=6)
        db = MyDB()
        db._executescript(query)
        filters = {'asset.cost__gt':gt, 'asset.cost__lt':lt}
        res = asset_queries.get_assets(filters=filters)
        assert len(res) == count


    @pytest.mark.parametrize("contains, count", [
        ('z', 0), ('o', 3), ('on', 1), ('thing', 4), ('things', 3), ('th', 4),
    ])
    def test_get_assets_filtering_4(self, setup_mydb, host, pagination, contains, count):
        """Should return the correct number of assets given search for text in description."""
        query = f"""
            insert into asset (id, asset_id, description, cost) values 
                (1, '1', 'one thing', 100), (2, '2', 'two things', 200), (3, '3', 'three things', 300),
                (4, '4', 'four things', 400), (5, '5', 'five', 500), (6, '6', 'six', 600);
        """
        pagination(page=0, limit=6)
        db = MyDB()
        db._executescript(query)
        filters = {'asset.description__contains':contains}
        res = asset_queries.get_assets(filters=filters)
        assert len(res) == count


    @pytest.mark.parametrize("gt, lt, contains, count", [
        (99, 601, 'th', 4), (99, 600, 'th', 4), (99, 400, 'th', 3),
        (500, 1000, 'six', 1), (1, 1000, 'something', 0), (200, 600, 'things', 2)
    ])
    def test_get_assets_filtering_5(self, setup_mydb, host, pagination, gt, lt, contains, count):
        """Should return the correct number of assets given 
        cost range and search for text in description."""
        query = f"""
            insert into asset (id, asset_id, description, cost) values 
                (1, '1', 'one thing', 100), (2, '2', 'two things', 200), (3, '3', 'three things', 300),
                (4, '4', 'four things', 400), (5, '5', 'five', 500), (6, '6', 'six', 600);
        """
        pagination(page=0, limit=6)
        db = MyDB()
        db._executescript(query)
        filters = {'asset.cost__gt':gt, 'asset.cost__lt':lt,
            'asset.description__contains':contains}
        res = asset_queries.get_assets(filters=filters)
        assert len(res) == count


    @pytest.mark.parametrize("contains1, contains2, count", [
        ('things', 'twee', 1), ('things', 'tw', 2), ('things', 'e t', 3), ('things', 're t', 1)
    ])
    def test_get_assets_filtering_6(self, setup_mydb, host, pagination, contains1, contains2, count):
        """Should return the correct number of assets given 
        multiple searches for text in description."""
        query = f"""
            insert into asset (id, asset_id, description, cost) values 
                (1, '1', 'one thing', 100), (2, '2', 'two things', 200), (3, '3', 'twee things', 300),
                (4, '4', 'fore things', 400), (5, '5', 'five', 500), (6, '6', 'six', 600);
        """
        pagination(page=0, limit=6)
        db = MyDB()
        db._executescript(query)
        filters = {'asset.description__contains':contains1, 
            'asset.description__contains':contains2}
        res = asset_queries.get_assets(filters=filters)
        assert len(res) == count


    @pytest.mark.parametrize("includes, count", [
        ([1000], 0), ([100], 1), ([500, 600], 2), ([500, 600, 700], 2), ([200, 250, 300, 400], 3)
    ])
    def test_get_assets_filtering_7(self, setup_mydb, host, pagination, includes, count):
        """Should return the correct number of assets that match the given set of costs."""
        query = f"""
            insert into asset (id, asset_id, description, cost) values 
                (1, '1', 'one thing', 100), (2, '2', 'two things', 200), (3, '3', 'three things', 300),
                (4, '4', 'four things', 400), (5, '5', 'five', 500), (6, '6', 'six', 600);
        """
        pagination(page=0, limit=6)
        db = MyDB()
        db._executescript(query)
        filters = {'asset.cost__includes':includes}
        res = asset_queries.get_assets(filters=filters)
        assert len(res) == count
    

    @pytest.mark.parametrize("gt, count", [
        ('2008-01-01 00:00:00', 6), ('2009-01-01 00:00:00', 5), ('2019-12-09 16:00:00', 0),
        ('2010-02-27 00:00:00', 2), ('2010-02-26 23:59:99', 3)
    ])
    def test_get_assets_filtering_8(self, setup_mydb, host, pagination, gt, count):
        """Should return the correct number of assets placed after a certain date."""
        query = f"""
            insert into asset (id, asset_id, description, date_placed) values 
                (1, '1', 'one',   '2009-01-01 00:00:00'), 
                (2, '2', 'two',   '2009-01-01 00:01:00'), 
                (3, '3', 'three', '2010-01-01 00:00:00'),
                (4, '4', 'four',  '2010-02-27 00:00:00'), 
                (5, '5', 'five',  '2016-01-01 00:00:00'), 
                (6, '6', 'six',   '2019-12-09 16:00:00');
        """
        pagination(page=0, limit=6)
        db = MyDB()
        db._executescript(query)
        filters = {'asset.date_placed__gt':gt}
        # similar to: select * from asset where datetime(date_placed) > datetime(f'{gt}');
        res = asset_queries.get_assets(filters=filters)
        assert len(res) == count
    

    @pytest.mark.parametrize("gt, lt, count", [
        ('2008-12-30 23:59:59', '2019-12-09 16:00:01', 6),
        ('2008-01-01 00:00:00', '2019-12-09 16:00:00', 5), 
        ('2008-01-01 00:00:00', '2016-01-01 00:00:00', 4),
        ('2009-01-01 00:00:00', '2016-01-01 00:00:00', 3),
    ])
    def test_get_assets_filtering_9(self, setup_mydb, host, pagination, gt, lt, count):
        """Should return the correct number of assets placed within a range of dates."""
        query = f"""
            insert into asset (id, asset_id, description, date_placed) values 
                (1, '1', 'one',   '2009-01-01 00:00:00'), 
                (2, '2', 'two',   '2009-01-01 00:01:00'), 
                (3, '3', 'three', '2010-01-01 00:00:00'),
                (4, '4', 'four',  '2010-02-27 00:00:00'), 
                (5, '5', 'five',  '2016-01-01 00:00:00'), 
                (6, '6', 'six',   '2019-12-09 16:00:00');
        """
        pagination(page=0, limit=6)
        db = MyDB()
        db._executescript(query)
        filters = {'asset.date_placed__gt':gt, 'asset.date_placed__lt':lt}
        res = asset_queries.get_assets(filters=filters)
        assert len(res) == count


    @pytest.mark.parametrize("loc_id, expected_sql, expected_params", [
        (7, "asset.id IN (?)", (1,)), (4, "asset.id IN (?, ?)", (1, 2)),
        (8, "asset.id IN (?)", (2,)), (5, "asset.id IN (?)", (6,)),
        (2, "asset.id IN (?, ?, ?)", (1, 2, 6)), (6, "asset.id IN (?)", (-1,)), 
        (3, "asset.id IN (?)", (6,)), (2, "asset.id IN (?, ?, ?)", (1, 2, 6)),
        (1, "asset.id IN (?, ?, ?)", (1, 2, 6))
    ])
    def test__get_sql_for_location_filter(self, setup_mydb, pagination, 
        loc_id, expected_sql, expected_params):
        """Should return correct sql and params to filter ids based on location."""
        # Locations as <loc_name>(<loc.id>:<asset.id>-<count>,<asset....):
        #
        #                           loc1(1)
        #                          /       \
        #                 building1(2)      building2(3:6-60)
        #                 /       \                |
        #           b1a(4:2-1)    b1b(5:6-40)     b2a(6)
        #              /   \
        # b1a_rm1(7:1-1)    b1a_rm2(8:2-2)
        query = f"""
            insert into location (id, description, parent) values
                (1, 'loc1', NULL),
                (2, 'building1', 1),
                (3, 'building2', 1),
                (4, 'b1a', 2),
                (5, 'b1b', 2),
                (6, 'b2a', 3),
                (7, 'b1a_rm1', 4),
                (8, 'b1a_rm2', 4);
            insert into asset (id, asset_id, description, bulk_count) values
                (1, '1', 'a', 1), (2, '2', 'b', 3), (3, '3', 'c', 1),
                (4, '4', 'd', 1), (5, '5', 'e', 1), (6, '6', 'f', 100);
            insert into location_count (asset, location, count) values
                (1, 7, 1), (2, 4, 1), (2, 8, 2), (6, 5, 40), (6, 3, 60);
        """
        db = MyDB()
        db._executescript(query)
        sql, params = asset_queries._get_sql_for_location_filter(loc_id)
        assert sql == expected_sql
        assert params == expected_params


    @pytest.mark.parametrize("location, expected_ids", [
        (7, [1]), (8, [2]), (4, [1, 2]), (5, [6]), (2, [1, 2, 6]),
        (1, [1, 2, 6]), (3, [6]), (6, [])
    ])
    def test_get_assets_filtering_10(self, setup_mydb, host, pagination, location, expected_ids):
        """Should return the correct number of assets based on location.
        Example: There are 40 of asset id 6 and 3 of asset id 2 in 'building1'."""
        # Locations as <loc_name>(<loc.id>:<asset.id>-<count>,<asset....):
        #
        #                           loc1(1)
        #                          /       \
        #                 building1(2)      building2(3:6-60)
        #                 /       \                |
        #           b1a(4:2-1)    b1b(5:6-40)     b2a(6)
        #              /   \
        # b1a_rm1(7:1-1)    b1a_rm2(8:2-2)
        query = f"""
            insert into location (id, description, parent) values
                (1, 'loc1', NULL),
                (2, 'building1', 1),
                (3, 'building2', 1),
                (4, 'b1a', 2),
                (5, 'b1b', 2),
                (6, 'b2a', 3),
                (7, 'b1a_rm1', 4),
                (8, 'b1a_rm2', 4);
            
            insert into asset (id, asset_id, description, bulk_count) values 
                (1, '1', 'one', 1), (2, '2', 'two', 3), (3, '3', 'three', 1),
                (4, '4', 'four', 1), (5, '5', 'five', 1), (6, '6', 'six', 100),
                (7, '7', 'seven', 1);
            
            insert into location_count (id, asset, location, count) values
                (1, 1, 7, 1), (2, 2, 8, 2), (3, 2, 4, 1), 
                (4, 6, 3, 60), (5, 6, 5, 40);
        """
        pagination(page=0, limit=5)
        db = MyDB()
        db._executescript(query)
        filters = {'location_count.location__eq':location}
        res = asset_queries.get_assets(filters=filters)
        ids = sorted([v['id'] for k, v in res.items()])
        assert ids == expected_ids

    ###############################################################################
    # ASSET FILTERING WITH COMBINATION OF ASSET FILTERS AND A LOCATION FILTER 
    ###############################################################################
    @pytest.mark.parametrize("location, cost, date, count, expected_ids", [
        # Only asset ids 1, 2, and 6 have assigned locations.
        # Asset ids 2, 3, 4 have cost 250 and ids 5, 6, and 7 have cost 1000.
        # Asset id 1 has cost 100.
        (1,  250, '2010-01-01 00:00:00', 0, []),
        (1,  250, '2010-01-02 00:00:00', 0, [2]), 
        (1,  250, '2010-01-02 00:00:00', 3, []), 
        (1,  250, '2010-01-02 00:00:00', 2, [2]),
        (1, 1000, '2010-01-02 00:00:00', 100, []),
        (1, 1000, '2010-01-02 00:00:00', 99, [6]),
        (1,  100, '2010-05-15 00:00:00', 0, []),
        (1,  100, '2010-05-15 00:00:01', 0, [1]),
        (2,  250, '2010-01-01 00:00:01', 2, [2]),
        (2, 1000, '2005-12-25 00:00:01', 99, [6]),
    ])
    def test_get_assets_filtering_11(self, setup_mydb, host, pagination, 
        location, cost, date, count, expected_ids):
        """Should return correct ids based on asset filters and location filters:
        location.id = ..., cost = ..., date_placed < ..., bulk_count > ..."""
        # Locations as <loc_name>(<loc.id>:<asset.id>-<count>,<asset....):
        #
        #                           loc1(1)
        #                          /       \
        #                 building1(2)      building2(3:6-60)
        #                 /       \                |
        #           b1a(4:2-1)    b1b(5:6-40)     b2a(6)
        #              /   \
        # b1a_rm1(7:1-1)    b1a_rm2(8:2-2)
        query = f"""
            insert into location (id, description, parent) values
                (1, 'loc1', NULL),
                (2, 'building1', 1),
                (3, 'building2', 1),
                (4, 'b1a', 2),
                (5, 'b1b', 2),
                (6, 'b2a', 3),
                (7, 'b1a_rm1', 4),
                (8, 'b1a_rm2', 4);
            
            insert into asset (id, asset_id, description, cost, date_placed, bulk_count) values 
                (1, '1', 'one',    100, '2010-05-15 00:00:00', 1), 
                (2, '2', 'two',    250, '2010-01-01 00:00:00', 3), 
                (3, '3', 'three',  250, '2009-08-11 00:00:00', 1),
                (4, '4', 'four',   250, '2009-01-01 00:00:00', 1), 
                (5, '5', 'five',  1000, '2001-01-31 00:00:00', 1), 
                (6, '6', 'six',   1000, '2005-12-25 00:00:00', 100),
                (7, '7', 'seven', 1000, '2007-10-09 00:00:00', 1);
            
            insert into location_count (id, asset, location, count) values
                (1, 1, 7, 1), (2, 2, 8, 2), (3, 2, 4, 1), 
                (4, 6, 3, 60), (5, 6, 5, 40);
        """
        pagination(page=0, limit=5)
        db = MyDB()
        db._executescript(query)
        filters = {'location_count.location__eq':location, 'asset.cost__eq':cost, 
            'asset.date_placed__lt':date, 'asset.bulk_count__gt':count}
        res = asset_queries.get_assets(filters=filters)
        ids = sorted([v['id'] for k, v in res.items()])
        assert ids == expected_ids

    @pytest.mark.parametrize("location, audit_date, count, expected_ids", [
        # Only asset ids 1, 2, and 6 have assigned locations.
        (1, '2018-01-01 00:00:00', 0, [2, 6]),
        (2, '2018-01-01 00:00:00', 0, [2, 6]),
        (4, '2018-01-01 00:00:00', 0, [2]),
        (7, '2018-01-01 00:00:00', 0, []),
        (8, '2018-01-01 00:00:00', 0, [2]),
        (5, '2018-01-01 00:00:00', 0, [6]),
        (3, '2018-01-01 00:00:00', 0, [6]),
        (6, '2018-01-01 00:00:00', 0, []),

        (1, '2019-01-01 00:00:00', 0, [2]),
        (2, '2019-01-01 00:00:00', 0, [2]),
        (4, '2019-01-01 00:00:00', 0, [2]),
        (7, '2019-01-01 00:00:00', 0, []),
        (8, '2019-01-01 00:00:00', 0, []),
        (5, '2019-01-01 00:00:00', 0, []),
        (3, '2019-01-01 00:00:00', 0, []),
        (6, '2019-01-01 00:00:00', 0, []),

        (1, '2020-01-01 00:00:00', 0, []),
        (2, '2020-01-01 00:00:00', 0, []),
        (4, '2020-01-01 00:00:00', 0, []),
        (7, '2020-01-01 00:00:00', 0, []),
        (8, '2020-01-01 00:00:00', 0, []),
        (5, '2020-01-01 00:00:00', 0, []),
        (3, '2020-01-01 00:00:00', 0, []),
        (6, '2020-01-01 00:00:00', 0, []),
    ])
    def test_get_assets_filtering_12(self, setup_mydb, host, pagination, 
        location, audit_date, count, expected_ids):
        """Should return correct ids based on asset filters and location filters:
        location.id = ..., cost = ..., date_placed < ..., bulk_count > ..."""
        # Locations as <loc_name>(<loc.id>:<asset.id>-<count>,<year>):
        #
        #                           loc1(1)
        #                          /       \
        #                 building1(2)      building2(3:6-60,19)
        #                 /          \                  |
        #           b1a(4:2-1,20)   b1b(5:6-40,19)     b2a(6)
        #              /      \
        # b1a_rm1(7:1-1,null) b1a_rm2(8:2-2,19)
        query = f"""
            insert into location (id, description, parent) values
                (1, 'loc1', NULL),
                (2, 'building1', 1),
                (3, 'building2', 1),
                (4, 'b1a', 2),
                (5, 'b1b', 2),
                (6, 'b2a', 3),
                (7, 'b1a_rm1', 4),
                (8, 'b1a_rm2', 4);
            
            insert into asset (id, asset_id, description, cost, date_placed, bulk_count) values 
                (1, '1', 'one',    100, '2010-05-15 00:00:00', 1), 
                (2, '2', 'two',    250, '2010-01-01 00:00:00', 3), 
                (3, '3', 'three',  250, '2009-08-11 00:00:00', 1),
                (4, '4', 'four',   250, '2009-01-01 00:00:00', 1), 
                (5, '5', 'five',  1000, '2001-01-31 00:00:00', 1), 
                (6, '6', 'six',   1000, '2005-12-25 00:00:00', 100),
                (7, '7', 'seven', 1000, '2007-10-09 00:00:00', 1);
            
            insert into location_count (id, asset, location, count, audit_date) values
                (1, 1, 7, 1,  null), 
                (2, 2, 8, 2,  '2019-01-01 00:00:00'), 
                (3, 2, 4, 1,  '2020-01-01 00:00:00'), 
                (4, 6, 3, 60, '2019-01-01 00:00:00'),
                (5, 6, 5, 40, '2019-01-01 00:00:00');
        """
        pagination(page=0, limit=5)
        db = MyDB()
        db._executescript(query)
        filters = {'location_count.location__eq':location, 
            'location_count.audit_date__gt':audit_date, 
            'location_count.count__gt':count}
        res = asset_queries.get_assets(filters=filters)
        ids = sorted([v['id'] for k, v in res.items()])
        assert ids == expected_ids

    
    @pytest.mark.parametrize("""location, audit_date, count, 
        expected_location_counts""", [
        # Only asset ids 1, 2, and 6 have assigned locations.
        (1, '2018-01-01 00:00:00', 1, 
            [[{'location_id': 8, 'count': 2, 'audit_date': '2019-01-01 00:00:00'}], 
            [{'location_id': 3, 'count': 60, 'audit_date': '2019-01-01 00:00:00'}, 
             {'location_id': 5, 'count': 40, 'audit_date': '2019-01-01 00:00:00'}]]
        ),
        (1, '2018-01-01 00:00:00', 3,
            [[{'location_id': 3, 'count': 60, 'audit_date': '2019-01-01 00:00:00'},
              {'location_id': 5, 'count': 40, 'audit_date': '2019-01-01 00:00:00'}]]
        ),
        (1, '2018-01-01 00:00:00', 40,
            [[{'location_id': 3, 'count': 60, 'audit_date': '2019-01-01 00:00:00'}]]
        ),
        (2, '2018-01-01 00:00:00', 3,
            [[{'location_id': 5, 'count': 40, 'audit_date': '2019-01-01 00:00:00'}]]
        ),
    ])
    def test_get_assets_filtering_13(self, setup_mydb, host, pagination, 
        location, audit_date, count, expected_location_counts):
        """Should return correct ids based on asset filters and location filters:
        location.id = ..., cost = ..., date_placed < ..., bulk_count > ..."""
        # Locations as <loc_name>(<loc.id>:<asset.id>-<count>,<year>):
        #
        #                           loc1(1)
        #                          /       \
        #                 building1(2)      building2(3:6-60,19)
        #                 /          \                  |
        #           b1a(4:2-1,20)   b1b(5:6-40,19)     b2a(6)
        #              /      \
        # b1a_rm1(7:1-1,null) b1a_rm2(8:2-2,19)
        query = f"""
            insert into location (id, description, parent) values
                (1, 'loc1', NULL),
                (2, 'building1', 1),
                (3, 'building2', 1),
                (4, 'b1a', 2),
                (5, 'b1b', 2),
                (6, 'b2a', 3),
                (7, 'b1a_rm1', 4),
                (8, 'b1a_rm2', 4);
            
            insert into asset (id, asset_id, description, cost, date_placed, bulk_count) values 
                (1, '1', 'one',    100, '2010-05-15 00:00:00', 1), 
                (2, '2', 'two',    250, '2010-01-01 00:00:00', 3), 
                (3, '3', 'three',  250, '2009-08-11 00:00:00', 1),
                (4, '4', 'four',   250, '2009-01-01 00:00:00', 1), 
                (5, '5', 'five',  1000, '2001-01-31 00:00:00', 1), 
                (6, '6', 'six',   1000, '2005-12-25 00:00:00', 100),
                (7, '7', 'seven', 1000, '2007-10-09 00:00:00', 1);
            
            insert into location_count (id, asset, location, count, audit_date) values
                (1, 1, 7, 1,  null), 
                (2, 2, 8, 2,  '2019-01-01 00:00:00'), 
                (3, 2, 4, 1,  '2020-01-01 00:00:00'), 
                (4, 6, 3, 60, '2019-01-01 00:00:00'),
                (5, 6, 5, 40, '2019-01-01 00:00:00');
        """
        pagination(page=0, limit=5)
        db = MyDB()
        db._executescript(query)
        filters = {'location_count.location__eq':location, 
            'location_count.audit_date__gt':audit_date, 
            'location_count.count__gt':count}
        res = asset_queries.get_assets(filters=filters)

        loc_groups = [v['location_counts'] for k, v in res.items()]
        assert loc_groups == expected_location_counts

    
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

    
