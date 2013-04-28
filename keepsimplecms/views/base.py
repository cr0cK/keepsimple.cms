# from pyramid.view import view_config

from ..models import DBSession


class ViewBase(object):
    """
    Base class for all views which provide helpers to manipulate the scope
    and other stuff.
    """

    # the scope is the dict sent to the template engine
    _scope = {
        'page_title': 'Sample title'
    }

    def __init__(self, request):
        self.request = request
        self.session = DBSession()

    def __call__(self):
        """
        Return the scope to render the template.
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


class View(ViewBase):
    """
    An another layer between the base and the view.
    Empty for the moment.
    """
    pass

