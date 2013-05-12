from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    UnicodeText,
    String,
    Enum
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from zope.sqlalchemy import ZopeTransactionExtension

Base = declarative_base()


class Route(Base):
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    pattern = Column(String(200))
    view = Column(String(200))

    def __init__(self, name, pattern, view):
        self.name = name
        self.pattern = pattern
        self.view = view


class Node(Base):
    __tablename__ = 'node'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True)
    type = Column(Enum('view', 'node'))
    template = Column(String(200))
    values = relationship("NodeValue", backref="node")

    def __init__(self, name, type, template):
        self.name = name
        self.type = type
        self.template = template


class NodeValue(Base):
    __tablename__ = 'node_value'

    id = Column(Integer, primary_key=True)
    key = Column(String(100))
    value = Column(UnicodeText())
    value_type_id = Column(Integer, ForeignKey('value_type.id'))
    node_id = Column(Integer, ForeignKey('node.id'))

    def __init__(self, key, value, value_type_id, node_id):
        self.key = key
        self.value = value
        self.value_type_id = value_type_id
        self.node_id = node_id


class ValueType(Base):
    __tablename__ = 'value_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    values = relationship("NodeValue", backref="type")

    def __init__(self, name):
        self.name = name
