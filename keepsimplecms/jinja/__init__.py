# -*- coding: utf-8 -*-

from .filters import filters
from .globals import functions


def register_functions(config):
    env = config.get_jinja2_environment()
    env.filters.update(filters)
    env.globals.update(functions)

