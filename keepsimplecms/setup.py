from keepsimplecms.models import Route, View as ViewModel
from keepsimplecms.view import View

def declare_routes(DBSession, config):
    views = DBSession.query(ViewModel).filter(ViewModel.type == 'View').all()

    # create views
    indexed_views = {}
    for view in views:
        indexed_views[view.name] = View.create(
            name=view.name,
            session=DBSession,
            template=view.template,
            values=view.values
        )

    # add routes
    for route in DBSession.query(Route).all():
        config.add_route(
            route.name,
            pattern=route.pattern,
            view=indexed_views[route.view]
        )
