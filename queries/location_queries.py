import sqlite3
from .db_path import DB_PATH

# TODO: need to test
def get_all_locations():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    query_select = """
        SELECT id, description, parent
        FROM location
        """

    print("got here")
    cur.execute(query_select)
    rows = cur.fetchall()
    conn.close()
    print("didn't get here?")
    
    ret = [
        {
            'id':id,
            'description':loc_desc,
            'parent':parent_id
        } 
        for id, loc_desc, parent_id in rows]
    return ret

