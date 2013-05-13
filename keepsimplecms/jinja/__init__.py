# -*- coding: utf-8 -*-

from .filters import filters
from .globals import functions


def register_functions(config):
    """
    Register globals and filters to the Jinja environment.
    """
    env = config.get_jinja2_environment()
    env.filters.update(filters)
    env.globals.update(functions)

