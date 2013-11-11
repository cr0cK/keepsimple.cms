# -*- coding: utf-8 -*-


class PlaceHolderException(Exception):
    pass


class PlaceHolder(object):
    _refs = {}

    @classmethod
    def get(cls, label):
        if label not in cls._refs:
            raise PlaceHolderException(
                'The label %s has not been found.' % label)
        return cls._refs[label]

    @classmethod
    def set(cls, label, ref):
        cls._refs[label] = ref
