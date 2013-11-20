from keepsimplecms.models import (Route,
                                  View as ViewModel)
from keepsimplecms.node import View
from keepsimplecms.node.factory import NodeFactory
from keepsimplecms.utils import PlaceHolder
from keepsimplecms.exceptions import SetupException


def declare_routes(config):
    session = PlaceHolder.get('session')

    # retrieve routes
    routes = session.query(Route).all()

    # retrieve views of all routes
    routes_views = [route.view for route in routes]
    views = session.query(ViewModel) \
        .filter(ViewModel.name.in_(routes_views)) \
        .all()

    # create nodess
    nodes = {}
    for view in views:
        nodes[view.name] = NodeFactory().create_from(model=view)().pop()

    # add routes
    for route in session.query(Route).all():
        try:
            view = nodes[route.view]
        except KeyError, e:
            raise SetupException('The view %s has not been found.' % route.view)

        config.add_route(
            route.name,
            pattern=route.pattern,
            view=nodes[route.view]
        )

    ### Declare Backoffice views and routes

    backoffice_views = {
        'BackOfficeHome': {
            'type': 'View',
            'template': 'templates/views/backoffice/home.html',
            'pattern': '/backoffice'
        }
    }

    for name, params in backoffice_views.items():
        nodes[name] = View.create(
            name=name,
            template=params['template'],
            scope={'layout': 'templates/layouts/backoffice/base.html'}
        )

        # split on upper case chars
        import re
        route_name = re.sub(r'([a-z])([A-Z])', r'\1-\2', name)

        config.add_route(
            route_name,
            pattern=params['pattern'],
            view=nodes[name]
        )

        config.add_static_view('static/backoffice',
            'backoffice:static/backoffice', cache_max_age=3600)

