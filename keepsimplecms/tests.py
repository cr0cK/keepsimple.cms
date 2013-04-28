import unittest

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views import home
        request = testing.DummyRequest()
        info = home.my_view(request)
        self.assertEqual(info['project'], 'keepsimple.cms')
