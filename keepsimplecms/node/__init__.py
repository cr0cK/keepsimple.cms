# -*- coding: utf-8 -*-

from pyramid.renderers import (render as py_render,
                              render_to_response as py_render_to_response)
from pyramid.url import route_url as py_route_url

from keepsimplecms.node.factory import NodeFactory
from keepsimplecms.utils import PlaceHolder


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

    """

    def __init__(self, name, ref, template, scope):
        """
        Create a new :class:`Node`.

        name

          Name of the node.

        ref

          Reference of the node.

        template

          Path of the template used for the rendering.

        scope

          Dict of values.

        """
        self.name = name
        self.ref = ref
        self.template = template
        self._scope = scope

    def scope(self, *arg, **kw):
        """
        Set values in the scope.

        .. code-block:: python

            view.scope('key')                  # get
            view.scope('key', 'value')         # set
            view.scope(key='value')            # set multiple values

        """

        # return all the scope
        if not len(arg) and not len(kw.keys()):
            return self._scope
        # return a value from the scope
        elif len(arg) == 1 and isinstance(arg[0], str):
            return self._scope.get(arg[0], '')
        # set only one value to the scope
        elif len(arg) == 2:
            self._scope[arg[0]] = arg[1]
        # set value(s) to the scope
        elif len(kw.keys()):
            for key, value in kw.iteritems():
                self._scope[key] = value

    @property
    def session(self):
        """
        Return the session object.

        """
        return PlaceHolder.get('session')

    @property
    def request(self):
        """
        Return the request object.

        """
        return PlaceHolder.get('request')

    def render(self):
        """
        Register helpers into the scope and call the customer render method.

        """
        self._register_methods_in_scope()
        self._render()

    def extend(self, **kwargs):
        """
        Extend the scope of the Node with other nodes.

        """
        for node in NodeFactory().create_from(**kwargs)():
            self.scope(**node.scope())

    def route_url(self, route_name, *elements, **kw):
        """
        Return an url of a route.

        """
        return py_route_url(route_name, self.request, *elements, **kw)

    def _register_methods_in_scope(self):
        """
        Register methods of the node into the scope.

        """
        # url generation
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


class View(Node):
    """
    Extend a :class:`Node` to create a view.

    """
    def __call__(self, context=None, request=None):
        """
        Make the class as a callable function.
        Called by Pyramid when this object is used as a view.

        The Pyramid context and request objects are pass by Pyramid and saved
        in the placeholder area.

        Return a Pyramid response object.

        """
        PlaceHolder.set('context', context)
        PlaceHolder.set('request', request)

        self.render()

        return py_render_to_response(self.template, self.scope(),
            request=self.request)
