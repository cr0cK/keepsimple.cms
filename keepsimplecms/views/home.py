from .base import View, Node


class Home(View):
    def render(self):
        self.scope('foo', 'bar')


class Test(View):
    def render(self):
        self.scope('foo', SampleNode(self.request)())


class SampleNode(Node):
    template = 'templates/sample_node.html'

    def render(self):
        self.scope('foo2', 'bar2')
