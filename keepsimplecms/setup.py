from keepsimplecms.models import Route, Node
from keepsimplecms.view import View

def declare_routes(DBSession, config):
    nodes = DBSession.query(Node).filter(Node.type == 'view').all()

    # create views
    views = {}
    for node in nodes:
        views[node.name] = View(session=DBSession, template=node.template,
            values=node.values)

    # add routes
    for route in DBSession.query(Route).all():
        config.add_route(
            route.name,
            pattern=route.pattern,
            view=views[route.view]
        )
