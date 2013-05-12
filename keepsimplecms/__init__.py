# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

from pyramid.renderers import render, render_to_response

from keepsimplecms.models import Node as NodeModel


class View(object):
    """
    Base class for all views and nodes.
    """

    _request = None
    _context = None
    # database session
    _session = None
    # template used for the rendering
    _template = None
    # dict sent to the template engine
    _scope = {}

    def __init__(self, request=None, session=None, template=None, values=None):
        """
        Save a reference to the Pyramid request object.
        """
        self._session = session
        self._template = template

        # save values
        self._scope = {}
        for value_ in values:
            key = value_.key
            value = value_.value

            if value_.type.name == 'node':
                key = '_' + key

            self.scope(key, value)

        self._init()

    def _init(self):
        """
        Post init function.
        Useful to set default values in the scope in sub classes.
        """
        pass

    def scope(self, *arg):
        """
        Get or set values in the scope.
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
        Set variables to the scope before rendering.

        To be extended by the view.
        """
        for k, v in self._scope.items():
            if k.startswith('_'):
                scope_variable = k[1:]
                node_name = v

                # retrieve the node
                node = self._session.query(NodeModel).filter(
                    NodeModel.name == node_name).first()

                if not node:
                    self._scope[scope_variable] = ('Node %s not found'
                        % node_name)
                else:
                    self._scope[scope_variable] = Node(
                        request=self._request, session=self._session,
                        template=node.template, values=node.values)()

    def __call__(self, context=None, request=None):
        """
        Make the class as a callable function.
        Return the scope.
        """
        if request:
            self._request = request
        if context:
            self._context = context

        self.render()

        return render_to_response(self._template, self._scope, request=self._request)


class Node(View):
    """
    A node is a View child which is not declared as a view. Therefore, a
    node is not mapped to an URL.

    A node represents a part of the HTML page and implements its own logic since
    the request and the DBSession objects are available.

    The page is build from several nodes, each ones should be independant and
    can be reused in different views.

    Since no view and route declaration is done for a node, a template must be
    declared.
    """
    def __call__(self):
        """
        Render the node from the template and scope values and return HTML.
        """
        self.render()

        if not self._template:
            return ''

        return render(self._template, self._scope, self._request)
