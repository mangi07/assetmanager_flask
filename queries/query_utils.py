# #########################################
# General purpose query utility functions.
# #########################################

import sqlite3
from .db_path import DB_PATH


def get_max_id(table):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"select max(id) from {table};")
    (max_id, ) = c.fetchone()
    conn.close()
    return max_id


def _list_categories(table, order_column):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"select * from {table} order by {order_column}")
    categories = c.fetchall()
    conn.close()
    return categories

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


# TODO: test
def parse_db_args_tuple(args):
    """
    args: tuple of format ('table', [('col1':val1,...)])
        where vals can be str, int, or float

    return: tuple (table name, column names, column values, question marks)
        eg: ('table', 'col1, col2', ('val1', 2), '?, ?')
    """
    table_name = args[0]
    cols = list(zip(args[1]))
    col_names = ', '.join(cols[0])
    col_vals = cols[1]
    col_prep = ', '.join('?'*len(col_names))

    return (table_name, col_names, col_vals, col_prep)


# TODO: finish and test
def parse_db_args_dict(args):
    """
    args: dict of format ('table', {'col1':val1,...})
        where vals can be str, int, or float

    return: tuple (table name, column names, column values, question marks)
        eg: ('table', 'col1, col2', ('val1', 2), '?, ?')
    """
    pass


# TODO: finish and test
def parse_db_args(args, args_format):
    """
    args: tuple or dict with info to be used to create new row in table
    args_format: 0 (for tuple) or 1 (for dict), governing which method to use to parse incoming args
    
    example tuple args: ('table', [('col1':val1,...)])
    example dict args:  ('table', {'col1':val1,...})
    """
    pass


# TODO: finish and test...finish reworking this function to allow associating, for example, one invoice with multiple assets
def db_add_m2m_assoc(assoc, m2m, table, a_ids):
    """
    assoc: tuple representing row to insert and associate with asset,
        eg: ('tablename', [('col1', 3), ('col2', 'abc')])
        Warning: Do not supply id.  This function will find the correct id for row to associate with asset.

    m2m: tuple representing table that links asset row and assoc
        eg: ('m2mtablename', [('col1', 3), ('col2', 'abc')])
        Warning: Only supply details of the relation.  This function will use the correct relation ids.

    table: the name of the table with existing entity
    return: True if successful, otherwise false
    """
    (assoc_table_name, col_names, col_vals, col_prep) = parse_db_args(assoc)
    (m2m_table_name, m2m_col_names, m2m_col_vals, m2m_col_prep) = parse_db_args(m2m)

    max_assoc_id = get_max_id(assoc_table_name)
    next_assoc_id = max_assoc_id + 1

    try:
        conn = sqlite3.connect(db_path)
        conn.set_trace_callback(print) # TODO: remove this log when done debugging/testing
        c = conn.cursor()
        c.execute(f"insert into {assoc_table_name} (id, {col_names}) 
            values (?, {col_prep});", 
            (next_assoc_id, ) + col_vals )
        c.execute(f"""insert into {m2m_table_name} (asset, {assoc_table_name}, {m2m_colnames}) 
            values (?, ?, {m2m_col_prep});""", 
            (a_id, next_assoc_id) + m2m_col_vals )
        # conn.commit() # TODO: uncomment once sql is tested and working properly
        conn.close()
        return True
    except:
        print(f"Failed to insert {file_table} associations into db.")
        return False