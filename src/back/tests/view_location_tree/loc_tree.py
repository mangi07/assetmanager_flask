from queries.location_queries import Locations

#from logger import log
# log("Testing log")

# optionally seed database with default data
from queries.query_utils import MyDB
query = f"""
    insert into location (id, description, parent) values
        (1, 'loc1', NULL),
        (2, 'building1', 1),
        (3, 'building2', 1),
        (4, 'b1a', 2),
        (5, 'b1b', 2),
        (6, 'b2a', 3),
        (7, 'b1a_rm1', 4),
        (8, 'b1a_rm2', 4);
"""
db = MyDB()
db._executescript(query)

locs = Locations()
locs.show_tree()
