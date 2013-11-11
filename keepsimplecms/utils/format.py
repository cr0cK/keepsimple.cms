# -*- coding: utf-8 -*-

import string
import unicodedata

def sanitize(unicode_str):
    return ''.join(x for x in unicodedata.normalize('NFKD', unicode_str)
        if x in string.ascii_letters).lower()
