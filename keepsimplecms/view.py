# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

import importlib
import inspect

from pyramid.renderers import render as render_to_html, render_to_response

from keepsimplecms.models import Node as NodeModel


class View(object):
    """
    Callable object which represents a view for a route and used as the base
    class for every node.

    _name

      Name of the view.

    _request

      Pyramid request object.
      Passed to each node when rendering.

    _context

      Pyramid context object.
      Passed to each node when rendering.

    _session

      Database session object.
      Passed to each node when rendering.

    _template

      Path to the template used for the rendering.
      The template is an attribute of the :class:`keepsimplecms.models.Node`
      model class.

    _scope

      Dictionary passed to the template.
      See :meth:`scope` to get and set values.

    """
    _name     = None
    _request  = None
    _context  = None
    _session  = None
    _template = None
    _scope    = {}

    def __init__(self, name=None, request=None, session=None, template=None,
        values=None, scope=None):
        """
        Create a new :class:`View`.

        Save references to differents objects.

        name

          Name of the view (or the Node).

        request

          Request object of the Pyramid framework.

        session

          Database session object.

        template

          Path of the template used for the rendering.

        values

          Each :class:`View`s and :class:`Node`s has optionnal values which are
          of different types (see :class:`ValueType`).
          Values of node type are saved as private attribute in the scope. When
          rendering, nodes are instanciated and called in order to get HTML code
          which is saved in a new scope attribute.

        scope

          @TODO
        """
        if name:
            self._name = name
        if request:
            self._request = request
        if session:
            self._session = session
        if template:
            self._template = template
        # Warning: force an empty dict if no scope is defined to avoid
        # deep recursion
        self._scope = scope if scope else {}

        # save values from the model into the scope
        if values:
            for value_ in values:
                key = value_.key
                value = value_.value

                if value_.type.name == 'node':
                    key = '_' + key

                self.scope(key, value)

    def scope(self, *arg):
        """
        Get or set values in the scope.

        .. code-block:: python

            view.scope('key')                  # get
            view.scope('key', 'value')         # set
            view.scope([{'key', 'value'},])    # set multiple values

        """
        # return a value from the scope
        if len(arg) == 1 and isinstance(arg[0], str):
            return self._scope.get(arg[0], '')
        # set only one value to the scope
        elif len(arg) == 2:
            self._scope[arg[0]] = arg[1]
        # set value(s) to the scope
        elif len(arg) == 1 and isinstance(arg[0], dict):
            for key, value in arg[0].iteritems():
                self._scope[key] = value

    def render(self):
        """
        Render each nodes saved as private attributes in the scope and save the
        rendering of nodes in new attributes.
        """
        self._render()

        # instanciate private attributes to nodes
        for k, v in self._scope.items():
            if not k.startswith('_'):
                continue

            scope_variable = k[1:]
            node_name = v

            # retrieve the node
            node = self._session.query(NodeModel).filter(
                NodeModel.name == node_name).first()

            if not node:
                self._scope[scope_variable] = ('Node %s not found'
                    % node_name)
            else:
                type_ = node.type

                # load dynamically the module and instanciate the node class
                if '.' in type_:
                    parts = type_.split('.')
                    class_node = parts.pop()
                    module_path = '.'.join(parts)
                    mod = importlib.import_module(module_path)
                    class_node = getattr(mod, class_node)
                else:
                    class_node = eval(type_)

                html = class_node(request=self._request, session=self._session,
                    template=node.template, values=node.values)()
                self.scope(scope_variable, html)

        # save the request object in the scope
        self.scope('request', self._request)

    def _render(self):
        """
        Set extra values in the scope.
        To be implemented by sub classes.
        """
        pass

    def node(self, name=None, values=None, scope=None):
        """
        Instanciate a node with an optionnal scope and return the HTML code.
        It's possible to pass either a class or a string as the node name,
        depending if the node is a custom implementation or is the generic
        Node object.
        For the two cases, node values are retrieved from the DB.

        name

          Name of a node (Class which extends :class:`Node` or a string)

        scope

          Scope to load in the node.

        """
        # try to guess the name and the type of the node
        if inspect.isclass(name):
            node_name = name.__class__.__name__
            node_type = name
        else:
            node_name = name
            node_type = Node

        # if no values has been passed, retrieve them
        if values is None:
            node = self._session.query(NodeModel).filter(
                    NodeModel.name == node_name).first()
            values = node.values if node else None

        return node_type(name=node_name, request=self._request,
            session=self._session, values=values, scope=scope)()

    def __call__(self, context=None, request=None):
        """
        Make the class as a callable function.
        Called by Pyramid when this object is used as a view in a route.

        The Pyramid context and request object are pass by Pyramid and saved
        in the view. Those objects are then passed to the nodes when rendering.

        Return a Pyramid response object.
        """
        if request:
            self._request = request
        if context:
            self._context = context

        self.render()

        return render_to_response(self._template, self._scope,
            request=self._request)


class Node(View):
    """
    Extend a :class:`View` to create a node.

    A node represents a part of the HTML page and implements its own logic since
    the request and the DBSession objects are available.

    The page is build from several nodes, each ones should be independant and
    can be reused in different views.

    A node is still a callable object but return the HTML code of the node
    instead of a response object.
    """
    def __call__(self):
        """
        Render the node from the template and scope attributes and return HTML.
        """
        self.render()

        # if no template has been defined, try to find it
        if not self._template:
            node_name = self._name or self.__class__.__name__
            node = self._session.query(NodeModel).filter(
                NodeModel.name == node_name).first()

            if node:
                self._template = node.template

            if not self._template:
                return 'Node "%s" has no template.' % node_name

        return render_to_html(self._template, self._scope, self._request)
