# ###################################
# Get asset listings, with filters,
# and with associated db entities.
# ###################################

from queries.query_utils import (
    MyDB,
    filters_to_sql,
    list_categories,
    list_manufacturers,
    list_suppliers,
    list_purchase_orders,
    list_departments,
    list_requisition_statuses,
    list_receiving_statuses,
)
from queries.location_queries import Locations
import config
from flask import request
import sqlite3
import config
from logger import log

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


def get_asset_pictures(ids):
    """Given a list of ids, get a list of corresponding pictures entries from db."""
    if len(ids) == 0:
        return {}
    
    host_url = config.get_host_url()

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

def get_asset_fars(ids):
    """Given a list of ids, get a list of corresponding invoice entries from db."""
    if len(ids) == 0:
        return {}

    query_select = """
        select asset_far.asset, far.id, far.description,
            far.pdf, far.life, far.start_date, far.amount,
            account.id, account.number, account.description
        from far
        left join asset_far on asset_far.far = far.id
        left join account on far.account = account.id
        where asset_far.asset in ({});
    """.format(','.join('?'*len(ids)))

    db = MyDB()
    params = tuple(ids)
    res = db.query(query_select, params)
    rows = res.fetchall()

    far_groups = {id:[] for id in ids}

    for a_id, f_id, description, pdf, life, start_date, amount,\
        acct_id, acct_num, acct_desc in rows:

        # TODO: determine whether to either....
        # (1) configure gunicorn dev mode like the following:
        #   gunicorn --log-level debug myapp:app
        # OR (2) use the flask dev server during development
        assert isinstance(amount, (int, float)), f"Amount {amount} is not a numeric type and therefore division cannot be used to convert or format the amount."

        far = {
            'id':f_id,
            'description':description,
            'pdf':pdf,
            'life':life,
            'start_date':start_date,
            'amount':amount/config.get_precision_factor(),
            'account_id':acct_id,
            'account_number':acct_num,
            'account_description':acct_desc,
        }
        far_groups[a_id].append(far)
    return far_groups

def get_asset_invoices(ids):
    """Given a list of ids, get a list of corresponding invoice entries from db."""
    if len(ids) == 0:
        return {}
    
    host_url = config.get_host_url()

    log("test ids:" + str(ids))
    query_select = """
        select asset_invoice.asset, invoice.id, invoice.number, invoice.file_path,
            invoice.total, asset_invoice.cost,invoice.notes
        from invoice
        left join asset_invoice on asset_invoice.invoice = invoice.id
        where asset_invoice.asset in ({});
    """.format(','.join('?'*len(ids)))

    db = MyDB()
    params = tuple(ids)
    res = db.query(query_select, params)
    rows = res.fetchall()

    invoice_groups = {id:[] for id in ids}

    for a_id, i_id, number, file_path, total, asset_amount, notes in rows:
        invoice = {
            'id':i_id,
            'number':number,
            'file_path':host_url + "file/" + file_path,
            'total':total/config.get_precision_factor() if total is not None else None,
            'asset_amount':asset_amount/config.get_precision_factor() if asset_amount is not None else None,
            'notes':notes,
        }
        invoice_groups[a_id].append(invoice)
    return invoice_groups

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
        asset.maint_dir,
        COUNT(asset.id) OVER () AS total_count
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
        if params is not None:
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
      Note that the maximum number of asset entries to be returned, the 'limit' in SQL, is set by a configuration value
      and is not the responsibility of this function.
    filters: dict of filters, example: {'asset.cost__gt':100} (see query_utils.filters_to_sql)

    Returns:
        tuple of ( <assets dict>, <total_count int> )
          where assets is the dict of asset entries by DB id -- restricted by pagination offset and limit --
          to be the subset of all possible asset entries that exist according to the same filters.
    """
    filters = {k:v for k,v in filters.items() if v is not None}
    # TODO: If filters contain location ids, modify query string in _get_asset_query_string
    #  and params before returning it here...or filter them out on in python on the tail end of this function
    location_groups = {}
    if [f for f in filters.keys() if 'location' in f]:
        location_groups = get_location_counts(filters)
        filters['asset.id__includes'] = list(location_groups.keys())
    
    query_string, params = _get_asset_query_string(page, filters)
    log(query_string)
    log(params)

    # Run db query
    db = MyDB()
    res = db.query(query_string, params)
    rows = res.fetchall()
    
    asset_ids = [row[0] for row in rows]
    location_groups = get_asset_locations(asset_ids)
    #location_groups = get_location_counts(filters)
    picture_groups = get_asset_pictures(asset_ids)
    invoice_groups = get_asset_invoices(asset_ids)
    far_groups = get_asset_fars(asset_ids)
    requisition_statuses = dict(list_requisition_statuses())
    receiving_statuses = dict(list_receiving_statuses())
    categories = dict(list_categories())
    manufacturers = dict(list_manufacturers())
    suppliers = dict(list_suppliers())

    total_count = 0 # remains 0 unless DB query returns at least 1 entity
    if len(rows) > 0:
        total_count = rows[0][-1]

    # combine rows per asset
    assets = {}
    for (id, asset_id, description, cost, cost_brand_new, shipping,
        is_current, requisition, receiving, category_1, category_2,
        model_number, serial_number, bulk_count, bulk_count_removed,
        date_placed, date_removed, date_record_created, date_warranty_expires,
        manufacturer, supplier, purchase_order,
        life_expectancy_years, notes, department, maint_dir, total_count) in rows:
        if id not in assets:
            assets[id] = {
                'id':id, 
                'asset_id':asset_id, 
                'description':description, 
                'cost':cost, 'cost_brand_new':cost_brand_new, 'shipping':shipping,
                'is_current':is_current == 1,
                'requisition':requisition_statuses[requisition] if requisition in requisition_statuses else None,
                'receiving':receiving_statuses[receiving] if receiving in receiving_statuses else None,
                'category_1':categories[category_1] if category_1 in categories else None,
                'category_2':categories[category_2] if category_2 in categories else None,
                'life_expectancy_years':life_expectancy_years,

                'model_number':model_number,
                'serial_number':serial_number,
                'manufacturer':manufacturers[manufacturer] if manufacturer in manufacturers else None,
                'supplier':suppliers[supplier] if supplier in suppliers else None,
                'date_warranty_expires':date_warranty_expires,

                'location_counts':{},
                'bulk_count':bulk_count,
                'bulk_count_removed':bulk_count_removed,
                'date_placed':date_placed,
                'date_removed':date_removed,

                'pictures':[],
                'invoices':[],
                'far':{}
            }
        assets[id]['location_counts'] = location_groups[id]
        assets[id]['pictures'] = picture_groups[id]
        assets[id]['invoices'] = invoice_groups[id]
        assets[id]['far'] = far_groups[id]

    # TODO: Should return an empty array if no assets are found based on page (offset in DB query)
    return assets, total_count
