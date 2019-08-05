from models import models
import sqlite3


class AssetController:
    def _getAssetRows(self, offset, count):
        conn = sqlite3.connect("assetsdb.sqlite3")
        cur = conn.cursor()
        cur.execute("SELECT id, asset_id, description FROM asset LIMIT ?, ?", [offset, count])
     
        rows = cur.fetchall()
     
        for row in rows:
            print(row)
        return rows
        
    def getAsset(self):
        # ###########################
        # refactor to obtain the following from sql queries
        # select * from asset limit <pagination offset>, <how many to fetch>;
        self._getAssetRows(0, 10)
        
        asset = models.Asset()
        asset.asset_id = "dummy_asset1"
        asset.description = "a;sdfkja;sdgha;sdjf;asdjf;asdfja;ljdfal;sdfja;sldjfa;sjgoiwnfasd;jf;salfj"
        
        pic1 = models.Picture()
        pic1.id = 1
        pic1.filepath = "media/truck.jpg"
        pic2 = models.Picture()
        pic2.id = 2
        pic2.filepath = "media/logo.png"
        asset_pics = [pic1, pic2]
        
        # Add locations before this point so recursive __str__ works on Location obj
        # sql query for all locations
        loc_count1 = models.LocationCount() # obtain from sql
        
        loc1 = models.Location()
        loc1.id = 1
        loc1.description = "test description"
        
        loc_count1.location = loc1 # obtain this object by id from in-memory location objs
        loc_count1.count = 5
        loc_count1.audit_date = None # date last audited
        counts = [loc_count1]
        # ###########################
        asset.pics = asset_pics
        asset.counts = counts

        return asset

# maybe adapt some of this code...
def insert_from_lists(mlists, column_names, mtable, mcursor):
    columns_str = list_to_column_names(column_names)
    
    params = "(" + ''.join( ["?, "]*(len(mlists[0])-1) ) + "?)"
    insert = "INSERT INTO {} ({}) VALUES {}".format(mtable, columns_str, params)
    vals = [tuple(vals_list) for vals_list in mlists]
    
    #insert_message(mtable, str(vals))
    cursor.executemany(insert, vals);
    conn.commit()