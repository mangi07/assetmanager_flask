###############################################################################
# File: test_queries_query_utils.py
# 
###############################################################################

from queries import query_utils
import sqlite3
import pytest

@pytest.fixture
def filter_operators():
    return {'eq':'=', 'gt':'>', 'lt':'<', 'contains':'LIKE', 'includes':'IN', 'is_null': None}


class TestQueryUtils:
    #######################################
    # test MyDB
    #######################################

    def test_MyDB_1(self, setup_mydb):
        db = query_utils.MyDB()
        db.query("insert into asset (id, asset_id, description) values (1, '1', 'desc');")
        result = db.query("select * from asset;")
        assert len(result.fetchall()) == 1

    #######################################
    # test filters WHERE clause formation
    #######################################
    def test__parse_filter_1(self):
        """Throws exception if filter is not correct form."""
        try:
            query_utils._parse_filter('blahblah', 100)
        except:
            assert True
            return
        assert False

    def test__parse_filter_2(self):
        """Parses filter correctly."""
        res = query_utils._parse_filter('table1.column1__filter1', 100)
        assert res == ('table1', 'column1', 'filter1', 100)

    def test__parse_filter_3(self):
        """Throws exception if filter is in partially correct form."""
        try:
            query_utils._parse_filter('table1.column1.filter1', 100)
        except:
            assert True
            return
        assert False

    def test__parse_filter_4(self):
        """Throws exception if filter is in partially correct form."""
        try:
            query_utils._parse_filter('table1__column1.filter1', 100)
        except:
            assert True
            return
        assert False

    def test__parse_filter_5(self):
        """Throws exception if filter is in partially correct form."""
        try:
            query_utils._parse_filter('table_one.column1_filter1', 100)
        except:
            assert True
            return
        assert False


    def test__validate_filters_1(self, filter_operators):
        """Should raise AssertionError since 'blah' is not a table in the database."""
        filters = [('blah', 'total', 'lt', '1000')]
        
        with pytest.raises(AssertionError, match='^Table'):
            query_utils._validate_filters(filters, filter_operators)

    def test__validate_filters_2(self, filter_operators, setup_mydb):
        """Should raise AssertionError since '1000' is not type int."""
        filters = [('invoice', 'total', 'lt', '1000')]
        with pytest.raises(AssertionError, match='^Value'):
            query_utils._validate_filters(filters, filter_operators)

    def test__validate_filters_3(self, filter_operators, setup_mydb):
        """Should raise AssertionError since column 'blah' is not in table 'asset'."""
        filters = [('asset', 'blah', 'eq', 'first thing')]
        with pytest.raises(AssertionError, match='^Column'):
            query_utils._validate_filters(filters, filter_operators)

    def test__validate_filters_4(self, filter_operators, setup_mydb):
        """Should not raise any errors since filters are correct."""
        filters = [('asset', 'description', 'eq', 'first thing'), ('invoice', 'total', 'lt', 1000)]
        query_utils._validate_filters(filters, filter_operators)

    def test__validate_filters_5(self, filter_operators, setup_mydb):
        """Should not raise any errors since filters are correct."""
        filters = [('asset', 'cost', 'gt', 100), ('asset', 'cost', 'lt', 1000), ('invoice', 'total', 'lt', 1000)]
        query_utils._validate_filters(filters, filter_operators)

    def test__validate_filters_6(self, filter_operators, setup_mydb):
        """Should raise AssertionError since one filter operator cannot be found."""
        filters = [('asset', 'cost', 'gt', 100), ('asset', 'cost', '<', 1000), ('invoice', 'total', 'lt', 1000)]
        with pytest.raises(AssertionError, match='^No equivalent'):
            query_utils._validate_filters(filters, filter_operators)

    def test_filters_to_sql_1(self):
        """Throws exception if argument is not a dict."""
        filters = None
        try:
            sql = query_utils.filters_to_sql(filters)
        except:
            assert True
            return
        assert False

    def test_filters_to_sql_2(self):
        """Returns empty string given empty dict."""
        filters = {}
        ret = query_utils.filters_to_sql(filters)
        assert ret == ("", [])

    def test_filters_to_sql_3(self):
        """Throws exception given incorrect filter name in the dict."""
        try:
            filters = {'blah_blah':25}
            ret = query_utils.filters_to_sql(filters)
        except:
            assert True
            return
        assert False

    def test_filters_to_sql_4(self):
        """Throws exception given 1 filter with valid name but invalid value."""
        filters = {'asset.cost__gt':'this is not a number!'}
        try:
            sql = query_utils.filters_to_sql(filters)
        except:
            assert True
            return
        assert False

    def test_filters_to_sql_5(self, setup_mydb):
        """Returns correct string given 1 valid filter in the dict."""
        filters = {'asset.cost__gt':1000}
        sql, params = query_utils.filters_to_sql(filters)
        assert sql == 'asset.cost > ?'
        assert params == [1000]

    def test_filters_to_sql_6(self, setup_mydb):
        """Returns correct string given 2 valid filters in dict, representing cost range."""
        filters = {'asset.cost__gt':1000, 'asset.cost__lt':2000}
        sql, params = query_utils.filters_to_sql(filters)
        assert sql == 'asset.cost > ? AND asset.cost < ?'
        assert params == [1000, 2000]

    def test_filters_to_sql_7(self, setup_mydb):
        """Returns correct string given valid search string in dict."""
        filters = {'asset.description__contains':'this thing'}
        sql, params = query_utils.filters_to_sql(filters)
        assert sql == "asset.description LIKE ?"
        assert params == ["%this thing%"]

    @pytest.mark.parametrize("is_current__includes, is_current__is_null, sql_expected, params_expected", 
            [
                (None, None, "", []),
                ([0,1], None, "asset.is_current IN (?, ?)", [0, 1]),
                ([0], None, "asset.is_current IN (?)", [0]),
                ([1], None, "asset.is_current IN (?)", [1]),
                ([0,1], None, "asset.is_current IN (?, ?)", [0,1]),
                ([1,1], None, "asset.is_current IN (?, ?)", [1,1]),
                ([0,0], None, "asset.is_current IN (?, ?)", [0,0]),
                (None, 0, "asset.is_current IS NULL", None),
            ]
        )
    def test_filters_to_sql_8(self, setup_mydb, 
            is_current__includes, is_current__is_null, sql_expected, params_expected):
        """Returns correct sql given filter(s) on is_current."""
        filters = {'asset.is_current__includes':is_current__includes, 
                'asset.is_current__is_null':is_current__is_null}
        sql, params = query_utils.filters_to_sql(filters)
        assert sql == sql_expected
        assert params == params_expected
    
    #######################################
    # test get_max_id
    #######################################

    def test_get_max_id_1(self, setup_mydb):
        """
        Given asset table with max id of 1,
        should return 1.
        """
        query = f"""
            insert into asset (id, asset_id, description) values 
                (1, 'assetone', 'something');
        """
        db = query_utils.MyDB()
        db.query(query)

        max_id = query_utils.get_max_id('asset')
        assert max_id == 1


    def test_get_max_id_2(self, setup_mydb):
        """
        Given asset table with max id of 3,
        should return 3.
        """
        query = f"""
            insert into asset (id, asset_id, description) values
                (1, 'a', 'a'), (2, 'b', 'b'), (3, 'c', 'c');
        """
        db = query_utils.MyDB()
        db.query(query)

        max_id = query_utils.get_max_id('asset')
        assert max_id == 3


    def test_get_max_id_3(self, setup_mydb):
        """
        Given table with 0 rows, max id should be 0.
        """
        max_id = query_utils.get_max_id('asset')
        assert max_id == 0

    def test__list_categories_1(self, setup_mydb):
        """
        Given table with 3 categories, should list them alphabetically.
        """
        query = f"""
            insert into department (name) values
                ('RECEIVING'), ('FINANCE'), ('MAINTENANCE');
        """
        db = query_utils.MyDB()
        db.query(query)

        cats = query_utils._list_categories('department', 'name')
        assert cats == [(2, 'FINANCE'), (3, 'MAINTENANCE'), (1, 'RECEIVING')]


    def test__list_categories_2(self, setup_mydb):
        """
        Given table with no entries, should return [].
        """
        cats = query_utils._list_categories('department', 'name')
        assert cats == []


    ################################################
    # m2m inserts
    ################################################

    def test__parse_db_args_dict_1(self):
        """
        Parses ('asset_invoice', [{'asset':1, 'cost':100}])
        Returns: ('asset_invoice', ['asset', 'cost'], [1, 100], '?, ?')
        """
        input = ('asset_invoice', [{'asset':1, 'cost':100}])
        (table, cols, vals, prep) = query_utils._parse_db_args_dict(input)
        assert table == 'asset_invoice'
        assert cols == 'asset, cost'
        assert vals == [(1, 100)]
        assert prep == '?, ?'


    def test__parse_db_args_dict_2(self):
        """
        Parses ('asset_invoice', [{'asset':1, 'cost':100}, {'asset':40, 'cost':150.29}])
        Returns: ('asset_invoice', 'asset, cost', [(1, 100), (40, 150.29)], '?, ?')
        """
        input = ('asset_invoice', [{'asset':1, 'cost':100}, {'asset':40, 'cost':150.29}])
        (table, cols, vals, prep) = query_utils._parse_db_args_dict(input)
        assert table == 'asset_invoice'
        assert cols == 'asset, cost'
        assert vals == [(1, 100), (40, 150.29)]
        assert prep == '?, ?'


    def test__parse_db_args_dict_3(self):
        """
        Parses ('asset_invoice', [])
        Throws error because list is empty.
        """
        input = ('asset_invoice', [])
        try:
            query_utils._parse_db_args_dict(input)
        except:
            assert True
            return
        assert False


    def test__parse_db_args_dict_4(self):
        """
        Parses ('asset_invoice', [{'asset':1, 'desc':'desc here'}, {'asset':40, 'desc':'desc here'}])
        Returns: ('asset_invoice', 'asset, desc', [(1, 'desc here'), (40, 'desc here'')], '?, ?')
        """
        input = ('asset_invoice', [{'asset':1, 'desc':'desc here'}, {'asset':40, 'desc':'desc here'}])
        (table, cols, vals, prep) = query_utils._parse_db_args_dict(input)
        assert table == 'asset_invoice'
        assert cols == 'asset, desc'
        assert vals == [(1, 'desc here'), (40, 'desc here')]
        assert prep == '?, ?'


    def test__parse_db_args_dict_5(self):
        """
        Parses ('asset_invoice', [{'asset':1, 'cost':100}, {'cost':150.29, 'asset':40}])
        Returns: ('asset_invoice', 'asset, cost', [(1, 100), (40, 150.29)], '?, ?'),
        even though keys are not in the same order between input dicts.
        """
        input = ('asset_invoice', [{'asset':1, 'cost':100}, {'cost':150.29, 'asset':40}])
        (table, cols, vals, prep) = query_utils._parse_db_args_dict(input)
        assert table == 'asset_invoice'
        assert cols == 'asset, cost'
        assert vals == [(1, 100), (40, 150.29)]
        assert prep == '?, ?'


    def test__parse_db_args_dict_6(self):
        """
        Parses ('asset_invoice', [{'asset':1, 'cost':100}, {'assets':40, 'cost':150.29}])
        Throws error because dicts do not contain the same set of keys.
        """
        input = ('asset_invoice', [{'asset':1, 'cost':100}, {'assets':40, 'cost':150.29}])
        try:
            query_utils._parse_db_args_dict(input)
        except:
            assert True
            return
        assert False


    def test__parse_db_args_dict_7(self):
        """
        Parses ('asset_invoice', [{'asset':1, 'cost':100}, {'assets':40}])
        Throws error because dicts do not contain the same number of pairs.
        """
        input = ('asset_invoice', [{'asset':1, 'cost':100}, {'assets':40}])
        try:
            query_utils._parse_db_args_dict(input)
        except:
            assert True
            return
        assert False


    def test_db_add_m2m_assoc_1(self, setup_mydb):
        new_row = ('invoice', 
            [{'number':3, 'file_path':'abc', 'total':100*10000000000, 'notes':'notes here'}])

        m2ms = ('asset_invoice', [{'asset':23, 'cost':40*10000000000}])

        query_utils.db_add_m2m_assoc(new_row, m2ms, 'invoice')

        db = query_utils.MyDB()
        result = db.query("select number, file_path, total, notes from invoice;")
        data = result.fetchall()
        assert data == [('3', 'abc', 1000000000000, 'notes here')]

        result = db.query("select asset, cost from asset_invoice;")
        data = result.fetchall()
        assert data == [(23, 400000000000)]


    def test_db_add_m2m_assoc_2(self, setup_mydb):
        new_row = ('invoice', 
            [{'number':3, 'file_path':'abc', 'total':100*10000000000, 'notes':'notes here'}])

        m2ms = ('asset_invoice', [
            {'asset':23,  'cost':40*10000000000},
            {'asset':101, 'cost':4000*10000000000}])

        query_utils.db_add_m2m_assoc(new_row, m2ms, 'invoice')

        db = query_utils.MyDB()
        result = db.query("select number, file_path, total, notes from invoice;")
        data = result.fetchall()
        assert data == [('3', 'abc', 1000000000000, 'notes here')]

        result = db.query("select asset, cost from asset_invoice;")
        data = result.fetchall()
        assert data == [(23, 400000000000), (101, 40000000000000)]
