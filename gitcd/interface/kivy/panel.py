import threading
import time

from kivy.uix.scrollview import ScrollView


class GitcdFakeNavigationPanel(object):
    def toggle_state(self):
        pass


class GitcdInlineNavigationPanel(ScrollView):

    def __init__(self, **kwargs):
        super(GitcdInlineNavigationPanel, self).__init__(**kwargs)
        threading.Thread(target=self.initialize).start()

    def initialize(self, **kwargs):
        while len(self.ids) <= 0:
            time.sleep(0.001)
        for id in self.ids:
            self.ids[id].panel = GitcdFakeNavigationPanel()
