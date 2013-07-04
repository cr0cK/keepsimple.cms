# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

import importlib

from pyramid.renderers import render as render_to_html, render_to_response

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


class View(object):
    """
    Callable object which represents a view for a route and used as the base
    class for every view.

    name

      Name of the view.

    template

      Path to the template used for the rendering.
      The template is an attribute of the :class:`keepsimplecms.models.View`
      model class.

    _scope

      Dictionary passed to the template.
      See :meth:`scope` to get and set values.

    _placeholder

      Dictionary passed from View to Nodes used to store context, request and
      session objects.

    """
    name         = None
    template     = None
    _scope       = {}
    _placeholder = {}

    def __init__(self, name, template, scope=None):
        """
        Create a new :class:`View`.

        name

          Name of the view.

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
            view.scope([{'key', 'value'},])    # set multiple values

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
        Render all nodes of the view saved as private attributes of the scope.

        """
        # instanciate private attributes to nodes
        for attribute, node_name in self.scope().items():
            if not attribute.startswith('_'):
                continue

            scope_variable = attribute[1:]

            # retrieve the views
            view_model = self.session.query(ViewModel).filter(
                ViewModel.name == node_name).first()
            node = Node.create_from_model(view_model)

            # save the node content in the scope
            self.scope(scope_variable, node())

        self._render()

    def _render(self):
        """
        Set extra values in the scope.
        To be implemented by sub classes.

        """
        pass

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

        return render_to_response(self.template, self.scope(),
            request=self.request)

    @classmethod
    def create(cls, name, template, values=None, scope=None, session=None):
        """
        Create a view.

        Values which are node type are saved as private attributes in the scope.
        While rendering, these attributes will be instanciated to nodes.

        Since nodes are views, the same things happen for nodes which allows to
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
                    key = '_' + key

                scope[key] = value

        return cls(
            name=name,
            template=template,
            scope=scope,
        )


class Node(View):
    """
    Extend a :class:`View` to create a node.

    A node represents a part of the HTML page and implements its own logic since
    the request and the DB session objects are available.

    A page is build from several nodes, each ones should be independant and
    should be reusable in different views.

    A node is a callable object and return HTML code.

    """
    def __call__(self):
        """
        Render the node from the template and scope attributes and return HTML.

        """
        self.render()

        return render_to_html(self.template, self.scope(), self.request)

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
