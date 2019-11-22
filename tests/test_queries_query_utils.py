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