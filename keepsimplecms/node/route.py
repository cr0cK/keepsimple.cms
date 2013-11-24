# -*- coding: utf-8 -*-

from keepsimplecms.utils import PlaceHolder
from pyramid.url import route_url as py_route_url


class Route(object):
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern

    def url(self, *args, **kw):
        return py_route_url(self.name, PlaceHolder.get('request'), *args, **kw)
