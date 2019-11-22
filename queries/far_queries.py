##############################
# FAR queries
##############################

import sqlite3
from .db_path import DB_PATH


def list_fars():
    """
    Lists all FAR entries,
    with: id, account_id, description, pdf, life, start_date, amount,
    sorted by account and then by pdf #'s within account.

    return: list of json-serializable dicts,
    eg: [{'id': 1, 'pdf': 123, 'description': 'thing', 
          'amount': 1.0, 'life_in_years': 5, 'start_date': '2019-01-01 00:00:00', 
          'account_id': 1, 'account_number': '16020', 'account_description': 'school'}]
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    query_select = """
        select far.id, far.pdf, far.description, far.amount/10000000000.0 as amount, far.life, far.start_date, 
        account.id as account_id, account.number as account_number, account.description as account_description 
        from far
        left join account on far.account = account.id
        order by account.number, far.pdf;
    """
    cur.execute(query_select)
    rows = cur.fetchall()
    conn.close()

    ret = [
        {
            'id':id,
            'pdf':pdf,
            'description':desc,
            'amount':amt,
            'life_in_years':life,
            'start_date':start,
            'account_id':acct_id,
            'account_number':acct_num,
            'account_description':acct_desc,
        } 
        for id, pdf, desc, amt, life, start, acct_id, acct_num, acct_desc in rows]
    return ret

