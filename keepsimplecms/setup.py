from keepsimplecms.models import Route, Node
from keepsimplecms.view import View

def declare_routes(DBSession, config):
    nodes = DBSession.query(Node).filter(Node.type == 'view').all()

    for route in DBSession.query(Route).all():
        for node in nodes:
            class_view = eval(node.type)
            view = class_view(session=DBSession, template=node.template,
                values=node.values)

            # add route
            config.add_route(
                route.name,
                pattern=route.pattern,
                view=view
            )


