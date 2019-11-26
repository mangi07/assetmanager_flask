###############################################################################
# File: test_queries_query_utils.py
# 
###############################################################################

from queries import query_utils
import sqlite3
import pytest

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
        #db_conn.executescript(query)
        #db_conn.close()

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
        #db_conn.executescript(query)
        #db_conn.close()

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
        #db_conn.executescript(query)
        #db_conn.close()

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
