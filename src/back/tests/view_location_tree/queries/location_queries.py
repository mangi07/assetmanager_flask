from collections import deque
# https://treelib.readthedocs.io/en/latest/
from treelib import Tree
from queries.query_utils import MyDB

class Location(object):
    def __init__(self, id, parent, description):
        self.id = id
        self.parent = parent
        self.description = description


class Locations(object):
    __instance = None

    def topological_sort(self, node_list):
        nodes_dict = {}
        node_deque = deque(node_list)
        while len(node_deque) > 0:
            node = node_deque.pop()
            if node["parent"] in nodes_dict: # parent in list ?
                nodes_dict[ node["id"] ] = node
            elif node["parent"] is None: # assuming there is only one node like this, the root node
                assert len(nodes_dict) == 0
                nodes_dict[ node["id"] ] = node
            else: # cannot add this node yet, so put it at the beginning
                node_deque.appendleft(node)
        return nodes_dict

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

        self._nodes_dict = self.topological_sort(self._list)

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
        for key, val in self._nodes_dict.items():
            node = Location(val['id'], val['parent'], val['description'])
            self._tree.create_node(
                tag=val['id'], 
                identifier=val['id'], 
                parent=val['parent'],
                #data=val['description']
                data=node
            )

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
        self._tree.show(data_property="description")
