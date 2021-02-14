###############################################################################
# File: test_queries_far_queries.py
# 
###############################################################################

from queries import far_queries
from queries.query_utils import MyDB
import sqlite3
import pytest

class TestFarQueries:

    def test_list_fars_1(self, setup_mydb):
        """
        Given 0 fixed asset register entries, should return None.
        """
        fars = far_queries.list_fars()
        assert fars == []

    def test_list_fars_2(self, setup_mydb):
        """
        Given 1 fixed asset register entry, should return correct fields.
        """
        query = f"""
            insert into account (id, number, description)
            values (1, '16020', 'school');
            
            insert into far (id, account, description, pdf, life, start_date, amount)
            values (1, 1, 'test', '123', 5, '2019-01-01 00:00:00', 10000000000);
        """
        db = MyDB()
        db._executescript(query)

        fars = far_queries.list_fars()
        assert fars == [{'id': 1, 'pdf': 123, 'description': 'test', 
            'amount': 1.0, 'life_in_years': 5, 'start_date': '2019-01-01 00:00:00', 
            'account_id': 1, 'account_number': '16020', 'account_description': 'school'}]


    def test_list_fars_3(self, setup_mydb):
        """
        Given 3 fixed asset register entries, should return correct fields in correct order.
        """
        query = f"""
            insert into account (id, number, description)
            values (1, '16020', 'school'), (2, '16021', 'maintenace');
            
            insert into far (id, account, description, pdf, life, start_date, amount)
            values (1, 2, 'third', '14', 5, '2019-01-03 00:00:00', 10000000000),
            (2, 1, 'first', '12', 5, '2019-01-01 00:00:00', 10000000000),
            (3, 2, 'second', '13', 5, '2019-01-02 00:00:00', 10000000000);
        """
        db = MyDB()
        db._executescript(query)

        fars = far_queries.list_fars()
        assert fars == [{'account_description': 'school',
             'account_id': 1,
             'account_number': '16020',
             'amount': 1.0,
             'description': 'first',
             'id': 2,
             'life_in_years': 5,
             'pdf': 12,
             'start_date': '2019-01-01 00:00:00'},
            {'account_description': 'maintenace',
             'account_id': 2,
             'account_number': '16021',
             'amount': 1.0,
             'description': 'second',
             'id': 3,
             'life_in_years': 5,
             'pdf': 13,
             'start_date': '2019-01-02 00:00:00'},
            {'account_description': 'maintenace',
             'account_id': 2,
             'account_number': '16021',
             'amount': 1.0,
             'description': 'third',
             'id': 1,
             'life_in_years': 5,
             'pdf': 14,
             'start_date': '2019-01-03 00:00:00'}]