# #########################################
# General purpose query utility functions.
# #########################################

import sqlite3
from .db_path import DB_PATH


class MyDB(object):
    __instance = None

    def __init__(self):
        self._conn = sqlite3.connect(DB_PATH)
        self._cursor = self._conn.cursor()

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def _query(self, funct, query, params=None):
        result = funct(query, params) if params is not None else funct(query)
        self._conn.commit()
        return result
        
    def query(self, query, params=None):
        """Returns a connection upon which fetchone or fetchmany may be called."""
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
        

def get_max_id(table):
    db = MyDB()
    result = db.query(f"select max(id) from {table};")
    (max_id, ) = result.fetchone()
    max_id = 0 if max_id == None else max_id
    
    return max_id


def _list_categories(table, order_column):
    #conn = sqlite3.connect(DB_PATH)
    #c = conn.cursor()
    #c.execute(f"select * from {table} order by {order_column}")
    #categories = c.fetchall()
    #conn.commit()
    #conn.close()
    db = MyDB()
    result = db.query(f"select * from {table} order by {order_column}")
    #return categories
    return result.fetchall()

def list_categories():
    return _list_categories(db_path, 'category', 'name')

def list_manufacturers():
    return _list_categories(db_path, 'manufacturer', 'name')

def list_suppliers():
    return _list_categories(db_path, 'supplier', 'name')

def list_purchase_orders():
    return _list_categories(db_path, 'purchase_order', 'number')

def list_departments():
    return _list_categories(db_path, 'department', 'name')

def list_accounts():
    return _list_categories(db_path, 'account', 'number')


################################################
# m2m inserts
################################################
def _parse_db_args_dict(args):
    """
    args: dict of format ('table', [{'col1':val1,...}])
        where vals can be str, int, or float

    return: tuple (table name, column names, column values, question marks)
        eg: ('table', 'col1, col2', ('val1', 2), '?, ?')
    

    Throws error if each dict does not contain the same number of pairs with the same set of keys
    
    Note: The order of keys supplied in each dict does not matter, as long as each dict
    contains the same set of keys.
    """
    table = args[0]
    rows = args[1]
    keys = sorted(rows[0].keys())
    vals = []
    for d in rows:
        v = [d[k] for k in keys]
        vals.append(tuple(v))
    cols = ', '.join(keys)
    col_prep = ', '.join('?'*len(keys))
    return (table, cols, vals, col_prep)


def db_add_m2m_assoc(assoc, m2ms, existing_col):
    """
    assoc: tuple representing new row to insert,
        eg: ('tablename', [{'col1':3, 'col2':'abc'}])
        Warning: Do not supply id.  This function will find the correct id for the new row.

    m2ms: tuple representing rows to insert into m2m table,
        eg: ('m2mtablename', [{'assoc_id':5, 'details_of_relation':'details here'}] )
        Warning: Caller only provides per association the existing id and details of association.

    existing_col: the column name in m2m table representing the existing entity

    return: True if successful, otherwise false
    """
    (assoc_table_name, col_names, col_vals, col_prep) = _parse_db_args_dict(assoc)
    (m2m_table_name, m2m_col_names, m2m_col_vals, m2m_col_prep) = _parse_db_args_dict(m2ms)

    max_assoc_id = get_max_id(assoc_table_name) # debug
    next_assoc_id = max_assoc_id + 1

    try:
        db = MyDB()
        db.query(f"""insert into {assoc_table_name} (id, {col_names}) 
            values (?, {col_prep});""", 
            (next_assoc_id, ) + col_vals[0] )

        # add id for associated table to each tuple of row values
        m2m_col_vals = [(next_assoc_id, ) + vals for vals in m2m_col_vals]
        db.query(f"""insert into {m2m_table_name} ({existing_col}, {m2m_col_names}) 
            values (?, {m2m_col_prep});""", m2m_col_vals )
        
        return True

    except Exception as e:
        print(e)
        print(f"Failed to insert m2m associations into db.")
        return False