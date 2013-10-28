import re

from keepsimplecms.models import Route, View as ViewModel
from keepsimplecms.view import View

def declare_routes(DBSession, config):
    # retrieve routes
    routes = DBSession.query(Route).all()

    # retrieve views of all routes
    routes_views = [route.view for route in routes]
    views = DBSession.query(ViewModel) \
        .filter(ViewModel.name.in_(routes_views)) \
        .all()

    # create views
    indexed_views = {}
    for view in views:
        indexed_views[view.name] = View.create(
            name=view.name,
            template=view.template,
            values=view.values,
            session=DBSession,
        )

    # add routes
    for route in DBSession.query(Route).all():
        config.add_route(
            route.name,
            pattern=route.pattern,
            view=indexed_views[route.view]
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
        indexed_views[name] = View.create(
            name=name,
            template=params['template'],
            scope={'layout': 'templates/layouts/backoffice/base.html'},
            session=DBSession,
        )

        # split on upper case chars
        route_name = re.sub(r'([a-z])([A-Z])', r'\1-\2', name)

        config.add_route(
            route_name,
            pattern=params['pattern'],
            view=indexed_views[name]
        )

        config.add_static_view('static/backoffice', 'backoffice:static/backoffice', cache_max_age=3600)

