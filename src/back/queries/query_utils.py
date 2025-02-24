# #########################################
# General purpose query utility functions.
# #########################################
from  logger import log
import sqlite3
from .db_path import DB_PATH

# TODO: optionally cache database schema 
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
        

def get_max_id(table):
    db = MyDB()
    result = db.query(f"select max(id) from {table};")
    (max_id, ) = result.fetchone()
    max_id = 0 if max_id == None else max_id
    
    return max_id


def _list_categories(table, order_column):
    db = MyDB()
    result = db.query(f"select * from {table} order by {order_column}")
    return result.fetchall()

def list_categories():
    """
    Returns:
        An array of (int, str) tuples: (cateogory id, name)
    """
    return _list_categories('category', 'name')

def list_manufacturers():
    """
    Returns:
        An array of (int, str) tuples: (mnf id, name)
    """
    return _list_categories('manufacturer', 'name')

def list_suppliers():
    """
    Returns:
        An array of (int, str) tuples: (supplier id, name)
    """
    return _list_categories('supplier', 'name')

def list_purchase_orders():
    """
    Returns:
        An array of (int, str) tuples: (id, purchase order)
    """
    return _list_categories('purchase_order', 'number')

def list_departments():
    """
    Returns:
        An array of (int, str) tuples: (department id, name)
    """
    return _list_categories('department', 'name')

def list_accounts():
    """
    Returns:
        An array of (int, str, str) tuples: (department id, name, description)
    """
    return _list_categories('account', 'number')

def list_requisition_statuses():
    """
    Returns:
        An array of (int, str) tuples: (status id, status)
    """
    return _list_categories('requisition', 'id')

def list_receiving_statuses():
    """
    Returns:
        An array of (int, str) tuples: (receiving id, status)
    """
    return _list_categories('receiving', 'id')



################################################
# filters - WHERE clause formation
################################################
# TODO: better validation needed on filters from the client: eg 'cost_lt' key should not cause internal server error 500
def _parse_filter(k, v):
    """
    Takes a key, value pair and returns a tuple of (table, column, filter, value)
    """
    split = k.split('.')
    print(f"\n\n{split}\n\n") # debug
    table = split[0]
    rem = split[1].split('__') # TODO: bug - this throws error if len(split) < 1 .. eg: k = "location"
    column = rem[0]
    f = rem[1]
    return table, column, f, v

def _validate_filters(fs, filter_operators):
    """
    Takes an array of (table, column, filter, value) and valid filter operators
    and compares each item against db schema to see if it makes sense.
    """
    # criteria
    db = MyDB()
    schemas = {}
    for table in list(set([t for t, c, f, v in fs])):
        schema = db.query(f"SELECT name, type from pragma_table_info('{table}')").fetchall()
        assert schema != [], f"Table {table} not in database!"
        schema = {k:v for k, v in schema}
        schemas[table] = schema

    # db data types
    types = {'INTEGER':int, 'TEXT':str, }

    # validation
    for t, c, f, v in fs:
        assert f in filter_operators, f"No equivalent db operator found for filter {f}!"
        assert c in schemas[t], f"Column {c} not in table {t}!"
        if f == 'is_null' and v == '':
            continue
        expected = types[schemas[t][c]] if f != 'includes' else list
        actual = type(v)
        assert expected == actual, \
            f"Value {str(v)} in table {t} is of type {str(expected)}.  Actual: {str(actual)}."


def filters_to_sql(filters):
    """
    filters: dict formed from GET params ...Example: "{'asset.cost__gt':100}"
    return: (string to append to sql WHERE, params) ...Example: ("asset.cost > ?", 100)
    
    Note: dates are expected in format 'yyyy-mm-dd hh:mm:ss' in order to make correct comparisons.
    If date formats are correct, the logic in string comparisons will work to make the correct comparison
    since the parts in this format are ordered from most to least significant, left to right. 
    """
    filters = {k:v for k,v in filters.items() if v is not None}
    filter_str = ""
    params_where = []
    one_or_more = False
    filter_operators = {'eq':'=', 'gt':'>', 'lt':'<', 'contains':'LIKE', 'includes':'IN', 'is_null': 'IS NULL'}

    fs = [_parse_filter(k, v) for k, v in filters.items()] if len(filters) > 0 else []
    _validate_filters(fs, filter_operators)

    for t, c, f, v in fs:
        v = f'%{v}%' if f == 'contains' else v
        prepared = f"({', '.join('?'*len(v))})" if f == 'includes' else '?'
        prepared = "" if f == 'is_null' else prepared
        filter_str += f'{t}.{c} {filter_operators[f]} {prepared} AND '
        if f == 'is_null':
            params_where = None
            continue
        else:
            params_where += v if type(v) is list else [v]
    filter_str = filter_str.strip(' AND ')
    log(params_where)
    return filter_str, params_where

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
