from .base import View

class Home(View):
    def render(self):
        self.scope('foo', 'bar')
