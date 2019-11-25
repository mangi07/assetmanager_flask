###############################################################################
# File: test_queries_query_utils.py
# 
###############################################################################

from queries import query_utils
import sqlite3
import pytest

class TestQueryUtils:

    # TODO: finish
    def test_get_max_id_1(self, db_conn):
        """
        Given asset table with max id of 1,
        should return 1.
        """
        query = f"""
            insert into asset (id, asset_id, description) values 
                (1, 'assetone', 'something');
        """
        db_conn.executescript(query)
        db_conn.close()

        max_id = query_utils.get_max_id('asset')
        assert max_id == 1

    def test_get_max_id_2(self, db_conn):
        """
        Given asset table with max id of 3,
        should return 3.
        """
        query = f"""
            insert into asset (id, asset_id, description) values
                (1, 'a', 'a'), (2, 'b', 'b'), (3, 'c', 'c');
        """
        db_conn.executescript(query)
        db_conn.close()

        max_id = query_utils.get_max_id('asset')
        assert max_id == 3

    def test_get_max_id_3(self, db_conn):
        """
        Given table with 0 rows, max id should be None.
        """
        max_id = query_utils.get_max_id('asset')
        assert max_id == None

    def test__list_categories_1(self, db_conn):
        """
        Given table with 3 categories, should list them alphabetically.
        """
        query = f"""
            insert into department (name) values
                ('RECEIVING'), ('FINANCE'), ('MAINTENANCE');
        """
        db_conn.executescript(query)
        db_conn.close()

        cats = query_utils._list_categories('department', 'name')
        assert cats == [(2, 'FINANCE'), (3, 'MAINTENANCE'), (1, 'RECEIVING')]

    def test__list_categories_2(self, db_conn):
        """
        Given table with no entries, should return [].
        """
        cats = query_utils._list_categories('department', 'name')
        assert cats == []

################################################
# m2m inserts
################################################
    def test__parse_db_args_dict_1(self, db_conn):
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
    
    def test__parse_db_args_dict_2(self, db_conn):
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
    
    def test__parse_db_args_dict_3(self, db_conn):
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

    def test__parse_db_args_dict_4(self, db_conn):
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
    
    def test__parse_db_args_dict_5(self, db_conn):
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
    
    def test__parse_db_args_dict_6(self, db_conn):
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

    def test__parse_db_args_dict_7(self, db_conn):
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