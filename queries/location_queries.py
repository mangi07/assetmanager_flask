import sqlite3


def get_all_locations():
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()

    query_select = """
        SELECT id, description, parent
        FROM location
        """

    cur.execute(query_select)
    rows = cur.fetchall()
    conn.close()
    
    ret = [
        {
            'id':id,
            'description':loc_desc,
            'parent':parent_id
        } 
        for id, loc_desc, parent_id in rows]
    return ret

