###############################################################################
# File: test_queries_asset_queries.py
#
###############################################################################

import pytest

from queries import location_queries
from queries.query_utils import MyDB

@pytest.fixture
def locations():
    # Locations as <loc_name>(<loc.id>:<asset.id>-<count>,<asset....):
    #
    #                           loc1(1)
    #                          /       \
    #                 building1(2)      building2(3:6-60)
    #                 /       \                |
    #           b1a(4:2-1)    b1b(5:6-40)     b2a(6)
    #              /   \
    # b1a_rm1(7:1-1)    b1a_rm2(8:2-2)
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

@pytest.fixture
def locations_deps_unsorted():
    # Locations as <loc_name>(<loc.id>):
    #
    #                           loc1(2)
    #                          /       \
    #                 building1(1)      building2(3)
    #                 /       \                |
    #              b1a(4)    b1b(5)          b2a(6)
    #              /   \
    #      b1a_rm1(7) b1a_rm2(8)

    # Records referr to parents that do not yet exist (ie: out of order topologically)
    query = f"""
        insert into location (id, description, parent) values
            (1, 'building1', 2),
            (2, 'loc1', NULL),
            (3, 'building2', 2),
            (4, 'b1a', 1),
            (5, 'b1b', 1),
            (6, 'b2a', 3),
            (7, 'b1a_rm1', 4),
            (8, 'b1a_rm2', 4);
    """
    db = MyDB()
    db._executescript(query)

class TestLocationQueries:
    def test_location_queries_1(self, setup_mydb, locations):
        """Should build the correct list of locations."""
        locs = location_queries.Locations()
        tree = locs.get_tree()
        assert tree == {
            1: {'children': 
                [{2: {'children': 
                    [{4: {'children': 
                        [{7: {'data': 'b1a_rm1'}}, 
                         {8: {'data': 'b1a_rm2'}}], 
                        'data': 'b1a'}}, 
                     {5: {'data': 'b1b'}}], 
                    'data': 'building1'}}, 
                 {3: {'children': 
                    [{6: {'data': 'b2a'}}], 'data': 'building2'}}
                ], 
               'data': 'loc1'
            }
        }

    def test_location_queries_1_deps_unsorted(self, setup_mydb, locations_deps_unsorted):
        """Should build the correct list of locations."""
        locs = location_queries.Locations()
        print("locs: ", locs.get_list())

        tree = locs.get_tree()
        assert tree == {
            2: {'children': 
                [{1: {'children': 
                    [{4: {'children': 
                        [{7: {'data': 'b1a_rm1'}}, 
                         {8: {'data': 'b1a_rm2'}}], 
                        'data': 'b1a'}}, 
                     {5: {'data': 'b1b'}}], 
                    'data': 'building1'}}, 
                 {3: {'children': 
                    [{6: {'data': 'b2a'}}], 'data': 'building2'}}
                ], 
               'data': 'loc1'
            }
        }

    @pytest.mark.parametrize("root, expected_ids", [
        (1, {1, 2, 3, 4, 5, 6, 7, 8}), 
        (2, {2, 4, 7, 8, 5}),
        (3, {3, 6}),
        (4, {4, 7, 8}),
        (5, {5}), (6, {6}), (7, {7}), (8, {8})
    ])
    def test_location_queries_2(self, setup_mydb, locations, root, expected_ids):
        """Should return the ids of the subtree of the given location."""
        locs = location_queries.Locations()
        ids = locs.get_subtree_ids(root)
        assert set(ids) == expected_ids
