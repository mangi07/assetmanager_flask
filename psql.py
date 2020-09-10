from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, create_engine, MetaData
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from collections import namedtuple
from functools import reduce

engine = create_engine('sqlite:///db.sqlite3')
Base = declarative_base()

 
class Asset(Base):
    __tablename__ = 'asset'
    id = Column(Integer, primary_key=True)
    description = Column(String)

    manufacturer = Column(Integer, ForeignKey('manufacturer.id'))
    manufacturer_rel = relationship("Manufacturer", back_populates="assets")

    locations = relationship("LocationCount", back_populates='asset_rel')


class Manufacturer(Base):
    __tablename__ = 'manufacturer'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    assets = relationship("Asset", order_by=Asset.id, back_populates="manufacturer_rel")


class LocationCount(Base):
    __tablename__ = 'location_count'
    id = Column(Integer, primary_key=True)
    asset = Column(Integer, ForeignKey('asset.id'), primary_key=True)
    location = Column(Integer, ForeignKey('location.id'), primary_key=True)
    count = Column(Integer, nullable=False)
    asset_rel = relationship("Asset", back_populates="locations")
    location_rel = relationship("Location", back_populates="assets")


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    
    parent = Column(Integer, ForeignKey('location.id'))
    parent_rel = relationship("Location", remote_side=[id])

    assets = relationship('LocationCount', back_populates='location_rel')


    def mtree(self):
        locs = []
        loc = self
        while(loc is not None):
            locs.append(loc.description)
            loc = loc.parent_rel
        return locs


    def _mtree2(self):
        root = None
        nodes = {}
        session = Session.object_session(self)
        Node = namedtuple('Node', ['location', 'children'])

        for loc in session.query(Location):
            nodes[loc.id] = Node(location=loc, children={})

        for loc in session.query(Location):
            p = loc.parent
            if p is not None:
                nodes[p].children[loc.id] = nodes[loc.id]
            else:
                root = nodes[loc.id]
        return root


    def print_tree(self):
        session = Session.object_session(self)
        root = self._mtree2()
        print(root.location.description)

        stack_A = []
        stack_B = []

        stack_A.append(root)

        #curr = root
        while len(stack_A) > 0:
            curr = stack_A[-1]
            tail_desc = curr.location.description + "(" + str(curr.location.id) + ")"
            s = ''.join([x.location.description + "(" + str(x.location.id) + ")" + " => " for x in stack_B]) + tail_desc
            print(s)
            if len(curr.children) > 0:
                stack_B.append(curr)
                stack_A.extend(list(curr.children.values()))
            else:
                stack_A.pop()
                if len(stack_A) == 0 or len(stack_B) == 0:
                    break

                while stack_A[-1] == stack_B[-1]:
                    stack_A.pop()
                    stack_B.pop()
                    if len(stack_A) == 0 or len(stack_B) == 0:
                        break
                
    
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

for instance in session.query(Location):
    instance.print_tree()
    break

#for instance in session.query(Asset):
#    for location_count in instance.locations:
#        print(location_count.location_rel.mtree())

#for instance in session.query(Location):
#    #print(instance.description, instance.parent_rel)
#    print(instance.mtree())
#
#for instance in session.query(Asset):
#    print(instance.manufacturer_rel.name)



