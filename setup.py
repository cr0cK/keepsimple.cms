import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='keepsimple.cms',
      version='0.1',
      description='A "keep simple CMS" over Pyramid."',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Alexis Mineaud',
      author_email='alexis.mineaud@gmail.com',
      url='https://github.com/cr0cK/keepsimple.cms',
      keywords='web pyramid pylons cms simple',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='keepsimplecms',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = keepsimplecms:main
      [console_scripts]
      initialize_keepsimple.cms_db = keepsimplecms.scripts.initializedb:main
      """,
      )
