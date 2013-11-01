# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

import importlib

from pyramid.renderers import (render as py_render,
                              render_to_response as py_render_to_response)
from pyramid.url import route_url as py_route_url

from keepsimplecms.models import View as ViewModel


def dynamic_import(class_name):
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


class Node(object):
    """
    A :class:`Node` is a callable object used as a view for Pyramid, which represents
    a part (a block or a node or whatever you want) of an HTML page.

    A node represents a part of the HTML page and implements its own logic since
    the request and the DB session objects are available.

    A page is build from several nodes, each ones should be independant and
    should be reusable in different views.

    A node is a callable object and return HTML code.

    name

      Name of the node.

    template

      Path to the template used for the rendering.
      The template is an attribute of the :class:`keepsimplecms.models.View`
      model class.

    _scope

      Dictionary passed to the template.
      See :meth:`scope` to get and set values.

    _placeholder

      Dictionary used to store context, request and session objects.

    """
    name         = None
    template     = None
    _scope       = {}
    _placeholder = {}

    def __init__(self, name, template, scope=None):
        """
        Create a new :class:`Node`.

        name

          Name of the node.

        template

          Path of the template used for the rendering.

        scope

          Dict of values.

        """
        self.name = name
        self.template = template
        self._scope = scope if scope else {}

    def scope(self, *arg):
        """
        Set values in the scope.

        .. code-block:: python

            view.scope('key')                  # get
            view.scope('key', 'value')         # set
            view.scope({'key': 'value'})       # set multiple values

        """
        # return all the scope
        if not len(arg):
            return self._scope
        # return a value from the scope
        elif len(arg) == 1 and isinstance(arg[0], str):
            return self._scope.get(arg[0], '')
        # set only one value to the scope
        elif len(arg) == 2:
            self._scope[arg[0]] = arg[1]
        # set value(s) to the scope
        elif len(arg) == 1 and isinstance(arg[0], dict):
            for key, value in arg[0].iteritems():
                self._scope[key] = value

    @property
    def session(self):
        """
        Return the session object.

        """
        return self._placeholder['session']

    @property
    def request(self):
        """
        Return the request object.

        """
        return self._placeholder['request']

    def render(self):
        """
        Render all nodes saved as private attributes in the scope.

        """
        def _instanciate(node_name):
            # retrieve the views
            view_model = self.session.query(ViewModel).filter(
                ViewModel.name == node_name).first()

            # save the node content in the scope
            return Node.create_from_model(view_model)

        # instanciate private attributes to nodes
        for attribute, node_name in self.scope().items():
            # if the attribute is not private, continue
            if not attribute.startswith('__'):
                continue

            key = attribute[2:]
            if isinstance(node_name, list):
                self.scope(key, [_instanciate(node) for node in node_name])
            else:
                self.scope(key, _instanciate(node_name))

        self._register_methods_in_scope()
        self._render()

    def route_url(self, route_name, *elements, **kw):
        """
        Return an url of a route.

        """
        return py_route_url(route_name, self.request, *elements, **kw)

    def _register_methods_in_scope(self):
        """
        Register methods of the node into the scope.

        """
        # url generating
        self.scope('_url', self.route_url)

    def _render(self):
        """
        Set extra values in the scope.
        To be implemented by sub classes.

        """
        pass

    def __call__(self):
        """
        Render the node from the template and scope attributes.

        """
        self.render()
        return py_render(self.template, self.scope(), self.request)

    @classmethod
    def create(cls, name, template, values=None, scope=None, session=None):
        """
        Create a :class:`Node`.

        Values of :class:`Node` type are saved as private attributes in the scope.
        While rendering, these attributes will be instanciated to :class:`Node`.

        Since Views are nodes, the same things happen for views which allows to
        build the entire page.

        """
        if session:
            cls._placeholder['session'] = session

        # save values from the model into the scope
        scope = scope or {}
        if values:
            for value_ in values:
                key = value_.key
                value = value_.value

                if value_.type.name == 'node':
                    key = '__' + key

                # if the key is already defined, append value into a list
                if key in scope:
                    if isinstance(scope[key], list):
                        scope[key].append(value)
                    else:
                        scope[key] = [scope[key], value]
                else:
                    scope[key] = value

        return cls(
            name=name,
            template=template,
            scope=scope,
        )

    @classmethod
    def create_from_model(cls, node_model):
        """
        Create a node from a model entry.

        """
        klass = dynamic_import(node_model.type)

        return klass.create(
            name=node_model.name,
            template=node_model.template,
            values=node_model.values,
        )


class View(Node):
    """
    Extend a :class:`Node` to create a view.

    """
    def __call__(self, context=None, request=None):
        """
        Make the class as a callable function.
        Called by Pyramid when this object is used as a view.

        The Pyramid context and request object are pass by Pyramid and saved
        in the placeholder area.

        Return a Pyramid response object.

        """
        self._placeholder['context'] = context
        self._placeholder['request'] = request

        self.render()

        return py_render_to_response(self.template, self.scope(),
            request=self.request)
