# ###################################
# Get asset listings, with filters,
# and with associated db entities.
# ###################################

from queries.query_utils import (MyDB, filters_to_sql,
list_categories,
list_manufacturers,
list_suppliers,
list_purchase_orders,
list_departments)
from queries.location_queries import Locations
from flask import request
import sqlite3
import config


# TODO: mark this function for possible future removal if not used
def get_asset_locations(ids):
    """Given a list of ids, get a list of corresponding location entries from db."""
    if len(ids) == 0:
        return {}

    query_select = """
        SELECT location_count.asset, location_count.id, location.id, location.description, location.parent, location_count.count, location_count.audit_date 
        FROM location_count
        LEFT JOIN location ON location_count.location = location.id
        WHERE location_count.asset IN ({});
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

def get_location_counts(filters=None):
    """
    filters: dict of filters
    Accepted filters: location_count.<column>__<operator from query_utils.filters_to_sql>
        Example: {'location_count.location__includes':[1,2,3],
            'location_count.audit_date__gt':'2000-05-01 14:00:00'} 
    """
    query = "SELECT asset, location, count, audit_date FROM location_count"
    params = None
    loc_filters = {}
    if filters:
        loc_filters = {k:v for k,v in filters.items() if 'location' in k}
        for k, v in loc_filters.items():
            filters.pop(k)
        if 'location_count.location__eq' in loc_filters:
            locs = Locations()
            loc_tree = locs.get_tree()
            loc_root_id = loc_filters['location_count.location__eq']
            loc_ids = locs.get_subtree_ids(loc_root_id)
            loc_filters.pop('location_count.location__eq')
            loc_filters['location_count.location__includes'] = loc_ids
    if loc_filters:
        q, p = filters_to_sql(loc_filters)
        if q != '':
            query += " WHERE " + q
            params = tuple(p)
    
    db = MyDB()
    res = db.query(query, params)
    rows = res.fetchall()

    asset_groups = {row[0]:[] for row in rows}
    for asset_id, location_id, count, audit_date in rows:
        asset_groups[asset_id].append({
            'location_id': location_id,
            'count': count,
            'audit_date': audit_date
        })
    return asset_groups


def _get_host_url():
    return request.host_url


def get_asset_pictures(ids):
    """Given a list of ids, get a list of corresponding pictures entries from db."""
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

def _get_pagination(page):
    limit = config.get_pagination_limit()
    offset = page * limit
    return offset, limit

def _get_sql_for_location_filter(loc_id):
    """
    Finds all asset ids associated with any node of the subtree of the location being filtered.
    The return value should be a tuple of (str, tuple): ('asset.id IN ({?,..})', ids)
    """
    locs = Locations()
    loc_tree = locs.get_tree()
    loc_ids = locs.get_subtree_ids(loc_id)
    db = MyDB()
    # TODO: refactor to filter on more than just location id
    ids = db.query(f"""SELECT asset FROM location_count 
        WHERE location IN ({', '.join('?'*len(loc_ids))})""", tuple(loc_ids))
    ids = sorted({id for (id,) in ids})
    
    if len(ids) > 0:
        prep = tuple(ids)
        sql = f"asset.id IN ({', '.join('?'*len(ids))})"
        return sql, tuple(ids)
    return "asset.id IN (?)", (-1,)

def _get_asset_query_string(page=0, filters=None):
    params_where = ()
    query_where = ""

    query_select = f"""
        SELECT asset.id, asset.asset_id, asset.description,
        asset.cost/{config.get_precision_factor()},
        asset.cost_brand_new/{config.get_precision_factor()}, 
        asset.shipping/{config.get_precision_factor()},
        asset.is_current,
        asset.requisition,
        asset.receiving,
        asset.category_1,
        asset.category_2,
        asset.model_number,
        asset.serial_number,
        asset.bulk_count,
        asset.bulk_count_removed,
        asset.date_placed,
        asset.date_removed,
        asset.date_record_created,
        asset.date_warranty_expires,
        asset.manufacturer,
        asset.supplier,
        asset.purchase_order,
        asset.life_expectancy_years,
        asset.notes,
        asset.department,
        asset.maint_dir
        FROM asset
    """

    if (filters):
        query_where = " WHERE "
        if 'location' in filters:
            loc_id = filters.pop('location')
            loc_q, loc_p = _get_sql_for_location_filter(loc_id)
            query_where += loc_q + ' AND '
            params_where += loc_p
        
        filter_str, params = filters_to_sql(filters)
        
        query_where += filter_str
        query_where = query_where.strip(' AND ')
        params_where += tuple(params)

        if query_where == " WHERE ":
            query_where = ""

    query_page = " LIMIT ?, ?"
    query_string = query_select + query_where + query_page
    params = params_where + _get_pagination(page)
    
    query_string = ' '.join(query_string.split()) + ';'
    return query_string, params


def get_assets(page=0, filters={}):
    """
    page: page number to determine offset of paginated results
    filters: dict of filters, example: {'asset.cost__gt':100} (see query_utils.filters_to_sql)
    """
    filters = {k:v for k,v in filters.items() if v is not None}
    # TODO: If filters contain location ids, modify query string in _get_asset_query_string
    #  and params before returning it here...or filter them out on in python on the tail end of this function
    location_groups = {}
    if [f for f in filters.keys() if 'location' in f]:
        location_groups = get_location_counts(filters)
        filters['asset.id__includes'] = list(location_groups.keys())
    
    query_string, params = _get_asset_query_string(page, filters)
    
    # Run db query
    db = MyDB()
    res = db.query(query_string, params)
    rows = res.fetchall()
    
    #asset_ids = [id for id, x, y, z in rows]
    asset_ids = [row[0] for row in rows]
    #location_groups = get_asset_locations(asset_ids)
    #location_groups = get_location_counts(filters)
    picture_groups = get_asset_pictures(asset_ids)
    # TODO: invoices and fars

    # combine rows per asset
    assets = {}
    for (id, asset_id, description, cost, cost_brand_new, shipping,
        is_current, requisition, receiving, category_1, category_2,
        model_number, serial_number, bulk_count, bulk_count_removed,
        date_placed, date_removed, date_record_created, date_warranty_expires,
        manufacturer, supplier, purchase_order,
        life_expectancy_years, notes, department, maint_dir) in rows:
        if id not in assets:
            assets[id] = {
                'id':id, 
                'asset_id':asset_id, 
                'description':description, 
                'cost':cost, 'cost_brand_new':cost_brand_new, 'shipping':shipping,
                'is_current':is_current == 1,
                
                'location_counts':{},
                'pictures':[],
                'invoices':[],
                'far':{}
            }
        assets[id]['location_counts'] = location_groups[id] if id in location_groups else {}
        assets[id]['pictures'] = picture_groups[id]

    return assets