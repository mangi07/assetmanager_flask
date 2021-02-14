import sqlite3
from treelib import Node, Tree
from queries.query_utils import MyDB


class Locations(object):
    __instance = None

    def __init__(self):
        query_select = """SELECT id, description, parent FROM location;"""
        db = MyDB()
        res = db.query(query_select)
        self._rows = res.fetchall()

        self._list = [
            {
                'id':id,
                'description':loc_desc,
                'parent':parent_id
            } 
            for id, loc_desc, parent_id in self._rows]

        # Locations as <loc_name>(<loc.id>:<asset.id>-<count>,<asset....)
        #
        #   Example tree:
        #                           loc1(1)
        #                          /       \
        #                 building1(2)      building2(3:6-60)
        #                 /       \                |
        #           b1a(4:2-1)    b1b(5:6-40)     b2a(6)
        #              /   \
        # b1a_rm1(7:1-1)    b1a_rm2(8:2-2)
        self._tree = Tree()
        for x in self._list:
            self._tree.create_node(tag=x['id'], identifier=x['id'], parent=x['parent'], data=x['description'])

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def get_tree(self):
        return self._tree.to_dict(with_data=True)

    def get_list(self):
        return { loc['id']:{'description':loc['description'], 'parent':loc['parent']} for loc in self._list }

    def get_subtree_ids(self, root_id):
        """Get a list of ints representing all ids under given id."""
        return [id for id in self._tree.expand_tree(nid=root_id)]

    def show_tree(self):
        self._tree.show()

