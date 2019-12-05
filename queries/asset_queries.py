# ###################################
# Get asset listings, with filters,
# and with associated db entities.
# ###################################

from queries.query_utils import MyDB, filters_to_sql
from flask import request
import sqlite3


def get_asset_locations(ids):
    if len(ids) == 0:
        return {}

    query_select = """
        SELECT location_count.asset, location_count.id, location.id, location.description, location.parent, location_count.count, location_count.audit_date 
        FROM location_count
        left join location on location_count.location = location.id
        WHERE location_count.asset in ({});
    """.format(','.join('?'*len(ids)))

    db = MyDB()
    params = tuple(ids)
    res = db.query(query_select, params)
    rows = res.fetchall()

    asset_groups = {id:[] for id in ids}
    for asset_id, loc_cnt_id, loc_id, loc_desc, loc_par, loc_cnt, audit_date in rows:
        asset_groups[asset_id].append({
            'count_id': loc_cnt_id,
            'location_id': loc_id,
            'description': loc_desc,
            'parent_id': loc_par,
            'count': loc_cnt,
            'audit_date': audit_date
        })
    return asset_groups


def _get_host_url():
    return request.host_url


def get_asset_pictures(ids):
    if len(ids) == 0:
        return {}
    
    host_url = _get_host_url()

    query_select = """
        select asset_picture.asset, picture.file_path from asset_picture
        left join picture on asset_picture.picture = picture.id
        where asset_picture.asset in ({});
    """.format(','.join('?'*len(ids)))

    db = MyDB()
    params = tuple(ids)
    res = db.query(query_select, params)
    rows = res.fetchall()

    pic_groups = {id:[] for id in ids}

    for id, path in rows:
        pic_groups[id].append(host_url + "img/" + path)
    return pic_groups

# TODO: functions: get_asset_fars, get_asset_invoices

def _get_pagination(page, limit):
    offset = page * limit
    return offset, limit

def get_assets(page=0, filters=None):
    # query string formation with optional filters
    params_where = ()
    query_select = """
        SELECT asset.id, asset.asset_id, asset.description, asset.cost
        FROM asset
    """
    
    query_where = ""
    #################################################
    if (filters):
        # TODO: pick up from here with query string formation for filters
        filter_str, params = filters_to_sql(filters)
        if len(filter_str) > 0:
            query_where += " WHERE " + filter_str
            params_where += params
    #################################################
    
    query_page = " LIMIT ?, ?"
    query_string = query_select + query_where + query_page
    params = params_where + _get_pagination(page, 5)

    # Run db query
    db = MyDB()
    res = db.query(query_string, params)
    rows = res.fetchall()
    
    import pprint
    asset_ids = [id for id, x, y, z in rows]
    location_groups = get_asset_locations(asset_ids)
    picture_groups = get_asset_pictures(asset_ids)
    # TODO: invoices and fars

    # combine rows per asset
    assets = {}
    for (id, asset_id, description, cost) in rows:
        if id not in assets:
            assets[id] = {
                'id':id, 
                'asset_id':asset_id, 
                'description':description, 
                'cost':cost,
                'location_counts':[],
                'pictures':[],
                'invoices':[],
                'far':{}
            }
        assets[id]['location_counts'] = location_groups[id]
        assets[id]['pictures'] = picture_groups[id]

    return assets