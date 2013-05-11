from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    String
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from zope.sqlalchemy import ZopeTransactionExtension

Base = declarative_base()


class Route(Base):
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    pattern = Column(String(200))
    view = Column(String(200))

    def __init__(self, name, pattern, view):
        self.name = name
        self.pattern = pattern
        self.view = view


class Node(Base):
    __tablename__ = 'node'

    id = Column(Integer, primary_key=True)
    type = Column(String(100))
    template = Column(String(200))
    values = relationship("NodeValue", backref="values")

    def __init__(self, type, template=None):
        self.type = type
        self.template = template


class NodeValue(Base):
    __tablename__ = 'node_value'

    id = Column(Integer, primary_key=True)
    node_id = Column(Integer, ForeignKey('node.id'))
    key = Column(String(100))
    value = Column(Text)

    def __init__(self, name, value):
        self.name = name
        self.value = value
