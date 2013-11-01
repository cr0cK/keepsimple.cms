# -*- coding: utf-8 -*-

from jinja2 import Environment
from jinja2.utils import Markup
from pprint import pformat
import sys
import types


env = Environment()


def global_node(node, indent=0, indent_first=False):
    """
    Used for the inclusion of a node (or several nodes) in a template by
    indenting and flagging the HTML string as safe.
    """
    if not node:
        return

    def info(node):
        """
        Display some information about a node.
        """
        attrs = ['name', 'template']
        infos = []
        for attr in attrs:
            infos.append('%s: %s' % (attr, getattr(node, attr)))
        return '<!--\n' + "\n".join(infos) + '\n-->\n'

    def render(node):
        """
        Return the node as HTML.
        """
        spaces = indent * 4
        tmpl = env.from_string(('{{ content | indent(%d, %s) }}' %
            (spaces, indent_first)))
        content = info(node) + node()
        html = tmpl.render(content=content)
        return html

    htmls = []
    if isinstance(node, list):
        htmls = [render(node_) for node_ in node]
    else:
        htmls = [render(node)]

    return Markup(''.join(htmls))

def global_dump(value):
    """
    Dump `value` for debugging.
    """
    tmpl = env.from_string('<pre>{{ value|forceescape }}</pre>')
    html = tmpl.render(value=pformat(value, 1, 2, 4))
    return Markup(html)

# save references to the defined functions
functions = {}
current_module = sys.modules[__name__]
for x in dir(current_module):
    x = current_module.__dict__.get(x)

    if isinstance(x, types.FunctionType) \
        and x.__name__.startswith('global_'):
        fn = '_' + x.__name__[len('global_'):]
        functions[fn] = x
