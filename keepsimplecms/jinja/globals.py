# -*- coding: utf-8 -*-

from jinja2 import Environment
from jinja2.utils import Markup
from pprint import pformat
import sys
import types


env = Environment()


def global_node(node_value, indent=0, indent_first=False):
    """
    Used for the inclusion of a node (or several nodes) in a template by
    indenting and flagging the HTML string as safe.
    """
    if not node_value:
        return

    def render(node_value):
        try:
            spaces = indent * 4
            tmpl = env.from_string(('{{ node_value | indent(%d, %s) }}' % (spaces, indent_first)))
            html = tmpl.render(node_value=node_value)
        except AttributeError:
            html = node_value
        return html

    htmls = []
    if isinstance(node_value, list):
        htmls = [render(node) for node in node_value]
    else:
        htmls = [render(node_value)]

    return Markup(''.join(htmls))


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
