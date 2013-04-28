from pyramid.config import Configurator
from pyramid_jinja2 import renderer_factory
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_renderer('.html', renderer_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route(u'home', u'/',)
    config.add_view(u'keepsimplecms.views.home.Home',
                    route_name=u'home',
                    renderer=u'templates/index.html')

    config.scan()

    return config.make_wsgi_app()
