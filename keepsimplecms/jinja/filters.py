# -*- coding: utf-8 -*-

import re
import sys
import types

import logging
log = logging.getLogger(__name__)


def filter_linebreaks(*args, **kwargs):
    """
    Convert \n to <br/>.

    """
    from django.utils.html import linebreaks
    return linebreaks(args[0])

def filter_match(*args, **kwargs):
    """
    Apply a regexp on a string and return a bool if no capture pattern
    is defined, or return a list of the matched patterns, or None if the
    regexp doesn't match anything.

    """
    args_list = list(args)
    args_list.reverse()
    searches = re.search(*args_list, **kwargs)
    if searches and len(searches.groups()) > 0:
        ret = searches.groups()
    elif searches and not searches.groups():
        ret = 1
    else:
        ret = None
    return ret


# save references to the defined functions
filters = {}
current_module = sys.modules[__name__]
for x in dir(current_module):
    x = current_module.__dict__.get(x)

    if isinstance(x, types.FunctionType) \
        and x.__name__.startswith('filter_'):
        fn = x.__name__[len('filter_'):]
        filters[fn] = x
