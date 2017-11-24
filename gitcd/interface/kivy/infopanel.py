import threading

import kivy
from kivy.lang import Builder

from kivy.uix.scrollview import ScrollView

from kivymd.list import ILeftBodyTouch, OneLineIconListItem
from kivymd.button import MDIconButton
from kivymd.card import MDCard


Builder.load_string('''
#:import MDSpinner kivymd.spinner.MDSpinner

<GitcdInfoPanel>:
    size_hint: None, None
    size: dp(320), dp(180)
    pos_hint: {'center_x': 0, 'center_y': 1}
    BoxLayout:
        orientation:'vertical'
        padding: dp(8)
        MDLabel:
            text: 'Title'
            theme_text_color: 'Secondary'
            font_style:"Title"
            size_hint_y: None
            height: dp(36)
        MDSeparator:
            height: dp(1)
        MDLabel:
            text: 'Body'
            theme_text_color: 'Primary'
''')


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class GitcdInfoPanel(MDCard):

    app = None
    branches = []
    tags = []

    def __init__(self, **kwargs):
        super(GitcdInfoPanel, self).__init__(**kwargs)
        threading.Thread(target=self.initialize).start()

    def initialize(self, **kwargs):
        pass
