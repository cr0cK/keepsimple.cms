class ViewBase(object):
    """
    Base class for all views and nodes.
    """

    # database session
    _session = None
    # the scope is the dict sent to the template engine
    _scope = {}

    def __init__(self, request=None):
        """
        Save a reference to the Pyramid request object.
        """
        self._request = request

    def __call__(self):
        """
        Make the class as a callable function witch can be rendered.
        """
        self.render()
        return self._scope

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

    def node(self, node):
        """
        Instanciate the :py:class:`Node` `node` and return its html code.
        """
        return node(self._request)()



class View(ViewBase):
    """
    Define the default variables in the scope.
    """
    _scope = {
        'layout': 'templates/layouts/default.html',
        'page_title': 'Sample title'
    }


class Node(ViewBase):
    """
    A node is a ViewBase child which is not declared as a view. Therefore, a
    node is not mapped to an URL.

    A node represents a part of the HTML page and implements its own logic since
    the request and the DBSession objects are available.

    The page is build from several nodes, each ones should be independant and
    can be reused in different views.

    Since no view and route declaration is done for a node, a template must be
    declared.
    """
    _template = None

    def __call__(self):
        self.render()

        if not self._template:
            return ''

        from pyramid.renderers import render
        return render(self._template, self._scope, self._request)
