import threading

import kivy
from kivy.lang import Builder

from kivy.uix.scrollview import ScrollView

from kivymd.list import ILeftBodyTouch, OneLineIconListItem
from kivymd.button import MDIconButton


Builder.load_string('''
#:import MDSpinner kivymd.spinner.MDSpinner

<GitcdBranchPanel>:
    do_scroll_x: False
    #pos_hint: {'center_x': 0.5, 'center_y': 0.45}
    size_hint: (0.3, 1)
    #size: 1, 1

    MDList:
        id: branch_list
        OneLineIconListItem:
            text: "test-branch"
            disabled: False
            IconLeftSampleWidget:
                icon: 'source-branch'
        OneLineIconListItem:
            text: "test-branch-1"
            disabled: False
            IconLeftSampleWidget:
                icon: 'source-branch'
        OneLineIconListItem:
            text: "test-branch-2"
            disabled: False
            IconLeftSampleWidget:
                icon: 'source-branch'
        OneLineIconListItem:
            text: "test-branch-3"
            disabled: False
            IconLeftSampleWidget:
                icon: 'source-branch'
        OneLineIconListItem:
            text: "test-branch-4"
            disabled: False
            IconLeftSampleWidget:
                icon: 'source-branch'
        OneLineIconListItem:
            text: "test-branch-5"
            disabled: False
            IconLeftSampleWidget:
                icon: 'source-branch'
''')


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class GitcdBranchPanel(ScrollView):

    app = None
    branches = []
    tags = []

    def __init__(self, **kwargs):
        super(GitcdBranchPanel, self).__init__(**kwargs)
        threading.Thread(target=self.initialize).start()

    def initialize(self, **kwargs):
        pass
