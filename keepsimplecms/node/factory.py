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
    """
    Factory which returns :class:`Node` objects.

    """
    _query = None
    _nodes = None
    _filter_fn = None
    _sorted_fn = None

    def create_from(self, **kw):
        """
        Save the query to create nodes from kwargs.

        """
        if 'model' in kw:
            self._nodes = self._create_from_model(kw.get('model'))

        else:
            self._query = PlaceHolder.get('session').query(ViewModel)
            valid_attributes = ('name', 'ref', 'type', 'model')
            filters = {}

            for attr, value in kw.items():
                if attr not in valid_attributes:
                    raise ViewException('%s must be one of these attributes: %s',
                        attr, (', '.join(valid_attributes)))

                self._query = self._query.filter(getattr(ViewModel, attr) == value)

        return self

    def _create_from_model(self, node_model):
        """
        Instanciate a node from a model.

        """
        node_type = _import(node_model.type)

        return node_type.create(
            name=node_model.name,
            ref=node_model.ref,
            template=node_model.template,
            values=node_model.values
        )

    def filter(self, fn):
        """
        Save the filter function.

        """
        self._filter_fn = fn
        return self

    def sorted(self, fn):
        """
        Save the sorted function.

        """
        self._sorted_fn = fn
        return self

    def __call__(self):
        """
        Execute the query, save nodes and return them.

        """
        if not self._nodes:
            self._nodes = [self._create_from_model(model)
                            for model in list(self._query)]

        if self._filter_fn:
            self._nodes = filter(self._filter_fn, self._nodes)

        if self._sorted_fn:
            self._nodes = sorted(self._nodes, key=self._sorted_fn)

        return self._nodes
