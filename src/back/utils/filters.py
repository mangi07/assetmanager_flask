
from logger import log

# TODO: asset.is_current may be better documented if a lookup table is added with: past (1), present (2), future (3),
#   but all is_current values would need to migrate as follows: 0 to 1, 1 to 2, null to 3

def map_req_bools(arr):
    return list( map(lambda s: True if s == 'true' else False, arr) )

def checkbox_group_filter(filters, column):
    """
    filters: list of booleans
    column: format <table>.<column> to be used to form filters dict key

    return: dict that can be used to filter table indicated in 'column' arg
    """
    filters = map_req_bools(filters)
    db_filters = {}

    # asset.is_current statuses in order: [past, present, unspecified - possibly not yet received or future asset]
        
    if all(filters) or not any(filters):
        return {} # ignoring this group of filters, since they are all True or all False


    included_statuses = []

    curr_status = 1
    for checked in filters:
        if checked:
            included_statuses.append(curr_status)
        curr_status += 1
   
    key = column + '__includes'
    db_filters[key] = included_statuses

    return db_filters



