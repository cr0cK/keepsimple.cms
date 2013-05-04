# -*- coding: utf-8 -*-

from jinja2.utils import Markup
from pprint import pformat
import sys
import types


def global_node(node_value):
    """
    Used for the inclusion of a node in a template.
    It just marks the node value `node_value` as safe.
    """
    return Markup(node_value)

def global_dump(value):
    """
    Dump `value` for debugging.
    """
    return Markup('<pre>' + pformat(value, 1, 2, 4) + '</pre>')


# save references to the defined functions
functions = {}
current_module = sys.modules[__name__]
for x in dir(current_module):
    x = current_module.__dict__.get(x)

    if isinstance(x, types.FunctionType) \
        and x.__name__.startswith('global_'):
        fn = x.__name__[len('global_'):]
        functions[fn] = x
