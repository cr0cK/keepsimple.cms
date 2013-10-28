# -*- coding: utf-8 -*-

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    UnicodeText,
    String,
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


class View(Base):
    __tablename__ = 'view'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), index=True)
    type = Column(String(100))
    template = Column(String(200))
    values = relationship("ViewValue", backref="view")

    def __init__(self, name, type, template):
        self.name = name
        self.type = type
        self.template = template


class ViewValue(Base):
    __tablename__ = 'view_value'

    id = Column(Integer, primary_key=True)
    key = Column(String(100))
    value = Column(UnicodeText())
    value_type_id = Column(Integer, ForeignKey('value_type.id'))
    view_id = Column(Integer, ForeignKey('view.id'))

    def __init__(self, key, value, value_type_id, view_id):
        self.key = key
        self.value = value
        self.value_type_id = value_type_id
        self.view_id = view_id


class ValueType(Base):
    __tablename__ = 'value_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    values = relationship("ViewValue", backref="type")

    def __init__(self, name):
        self.name = name
