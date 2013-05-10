# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

from pyramid.renderers import render, render_to_response


class View(object):
    """
    Base class for all views and nodes.
    """

    # database session
    _session = None
    # the template used for the rendering
    _template = None
    # the scope is the dict sent to the template engine
    _scope = {}

    def __init__(self, request=None):
        """
        Save a reference to the Pyramid request object.
        """
        self._request = request
        self._scope = {}
        self._init()

    def _init(self):
        """
        Post init function.
        Useful to set default values in the scope in sub classes.
        """
        pass

    def scope(self, *arg):
        """
        Getter/setter to the scope.
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
        pass

    def node(self, node_class, values=None):
        """
        Instanciate the :py:class:`Node` `node` with optional `values`
        and return its html code.
        """
        node = node_class(request=self._request, session=self._session,
            values=values)
        node.scope('_node', type(self))
        return node()

    def __call__(self):
        """
        Make the class as a callable function.
        Return the scope.
        """
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

    def __init__(self, request=None, session=None, values=None):
        """
        Save a reference to the Pyramid request object,
        a reference to the DB session and merge optionnal
        values in the scope.
        """
        super(Node, self).__init__(request=request)
        self._session = session
        if values:
            self.scope(values)

    def __call__(self):
        """
        Render the node from the template and scope values and return HTML.
        """
        self.render()

        if not self._template:
            return ''

        return render(self._template, self._scope, self._request)


# class NodePlaceHolder(object):
#     _nodes = {}
#
#     @classmethod
#     def save(self, node_name, node_object):
#         """
#         ...
#         """
#         # @TODO check node type ?
#         self._nodes[node_name] = node_object
#
#     def __call__(self, node_name):
#         """
#         ...
#         """
#         if not self._nodes.has_key(node_name):
#             log.error('The node %s has not been found.', node_name)
#
#         return self._nodes.get(node_name, Node())

