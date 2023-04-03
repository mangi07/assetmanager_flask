# #########################################
# General purpose query utility functions.
# #########################################
from  logger import log
import sqlite3
from .db_path import DB_PATH
#from pathlib import Path


class MyDB(object):
    __instance = None

    def __init__(self):
        #assert Path(DB_PATH).exists()
        self._conn = sqlite3.connect(DB_PATH)
        self._cursor = self._conn.cursor()
        
        #######################################################################
        # PRAGMA database_list;
        
        # This pragma works like a query to return one row for each database 
        # attached to the current database connection.

        # The second column is "main" for the main database file, "temp" for 
        # the database file used to store TEMP objects, or the name of the 
        # ATTACHed database for other database files.

        # The third column is the name of the database file itself, or an empty string 
        # if the database is not associated with a file.
        #######################################################################
        self._cursor.execute("PRAGMA database_list")
        rows = self._cursor.fetchall()
        for row in rows:
            # show which database is to be queried
            print(row[0], row[1], row[2])
        #######################################################################

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def _query(self, funct, query, params=None):
        result = funct(query, params) if params is not None else funct(query)
        self._conn.commit()
        return result
        
    def query(self, query, params=None):
        """
        Returns a connection upon which fetchone or fetchmany may be called.
        You may supply either:
        (1) A prepared statement - query with question marks and corresponding params OR
        (2) Just a query without params.
        """
        if isinstance(params, tuple):
            return self._query(self._cursor.execute, query, params)
        elif isinstance(params, list):
            return self._query(self._cursor.executemany, query, params)
        elif params is None:
            return self._query(self._cursor.execute, query)

    def _executescript(self, query):
        """For testing setup purposes only."""
        self._cursor.executescript(query)
        self._conn.commit()

    def __del__(self):
        self._cursor.close()
        self._conn.close()

