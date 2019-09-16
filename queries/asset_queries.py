import sqlite3


def get_assets(page=0, filters=None):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()

    # TODO: extract query string formation out to testable function

    # pagination
    limit = 5
    offset = page * limit
    params_page = [offset, limit]

    # query string formation with optional filters
    cost_precision = 10000000000
    params_where = []
    query_select = """
        SELECT asset.id, asset.asset_id, asset.description, asset.cost, 
        location.id, location.description, location_count.count, location_count.audit_date,
        picture.file_path, invoice.number, invoice.file_path, purchase_order.number 
        FROM asset 
        left join location_count on location_count.asset = asset.id
        left join location on location_count.location = location.id
        left join asset_picture on asset_picture.asset = asset.id
        left join picture on asset_picture.picture = picture.id
        left join asset_invoice on asset_invoice.asset = asset.id
        left join invoice on asset_invoice.invoice = invoice.id
        left join purchase_order on asset.purchase_order = purchase_order.id
        """
    query_where = ""
    if (filters):
        #print(filters)
        filter_str = ""
        one_or_more = False

        cost_gt = filters.get('cost_gt')
        if cost_gt:
            filter_str += " asset.cost > ? "
            params_where.append(cost_gt * cost_precision)
            one_or_more = True

        cost_lt = filters.get('cost_lt')
        if cost_lt:
            mand = " AND " if one_or_more else ""
            filter_str += mand + " asset.cost < ? "
            params_where.append(cost_lt * cost_precision)
            one_or_more = True

        location_id = filters.get('location')
        if location_id:
            loc = " AND " if one_or_more else ""
            filter_str += loc + " location.id = ? "
            params_where.append(location_id)
            one_or_more = True
        # add more filters here in a similar manner

        if len(filter_str) > 0:
            query_where += " WHERE " + filter_str
    query_limit = " LIMIT ?, ?"
    query_string = query_select + query_where + query_limit
    params = params_where + params_page
    #print(query_string)
    #print(params)

    cur.execute(query_string, params)
    rows = cur.fetchall()
    conn.close()
    
    # combine rows per asset
    precision = 10000000000
    assets = {}
    for (id, asset_id, description, cost,
        loc_id, loc_desc, loc_count, loc_audit_date,
        pic_path, inv_num, inv_path, po_num) in rows:
        if id not in assets:
            assets[id] = {
                'id':id, 
                'asset_id':asset_id, 
                'description':description, 
                'cost':None if cost is None else float(cost/precision),
                'location_counts':{},
                'pictures':{},
                'invoices':{},
                'purchase_order':po_num,
            }
        assets[id]['location_counts'][loc_id] = {
            'description':loc_desc,
            'count':loc_count,
            'audit_date':loc_audit_date
        }


    precision = 10000000000
    # ret = [
    #     {
    #         'id':id, 
    #         'asset_id':asset_id, 
    #         'description':description, 
    #         'cost':None if cost is None else float(cost/precision),
    #         'location':{
    #             'id':loc_id,
    #             'description':loc_desc
    #         }
    #     } 
    #     for id, asset_id, description, cost, loc_id, loc_desc in rows]
    return assets