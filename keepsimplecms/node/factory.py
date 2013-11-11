# -*- coding: utf-8 -*-

import importlib

from keepsimplecms.utils import PlaceHolder
from keepsimplecms.models import View as ViewModel


def _import(class_name):
    """
    Import dynamically a class in a module.

    class_name

      Name of the class.

    """
    parts = class_name.split('.')
    class_name = parts.pop()

    if len(parts):
        try:
            module_path = '.'.join(parts)
            mod = importlib.import_module(module_path)
            klass = getattr(mod, class_name)
        except AttributeError:
            raise Exception('The %s has not been found in the module %s.' % (
                class_name, mod.__name__))
    else:
        klass = eval(class_name)

    return klass


class NodeFactory(object):
    _query = None

    def create_from(self, **kwargs):
        """
        Factory which returns :class:`Node` objects from a node attribute.

        """
        self._query = PlaceHolder.get('session').query(ViewModel)

        valid_attributes = ('name', 'ref', 'type')
        filters = {}
        for attr, value in kwargs.items():
            if attr not in valid_attributes:
                raise ViewException('%s must be one of these attributes: %s',
                    attr, (', '.join(valid_attributes)))

            self._query = self._query.filter(getattr(ViewModel, attr) == value)

        return [self.create_from_model(view_model) for view_model in list(self._query)]

    @classmethod
    def create_from_model(cls, node_model):
        """
        Create a node from a model entry.

        """
        cls_ = _import(node_model.type)

        return cls_.create(
            name=node_model.name,
            ref=node_model.ref,
            template=node_model.template,
            values=node_model.values
        )

