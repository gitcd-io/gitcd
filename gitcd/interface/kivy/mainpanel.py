import threading

import kivy
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout

from kivymd.list import ILeftBodyTouch, OneLineIconListItem
from kivymd.button import MDIconButton
from kivymd.tabs import MDTabbedPanel


Builder.load_string('''
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDTab kivymd.tabs.MDTab
#:import GitcdBranchPanel gitcd.interface.kivy.branchpanel.GitcdBranchPanel
#:import GitcdTagPanel gitcd.interface.kivy.tagpanel.GitcdTagPanel

<GitcdMainPanel>:
    id: main_panel
    spacing: 20
    MDTabbedPanel:
        id:tab_panel
        size_hint: (0.4, 1)
        tab_display_mode:'text'
        MDTab:
            name: 'branches'
            text: "Branches" # Why are these not set!!!
            GitcdBranchPanel:
                id: branch_panels
        MDTab:
            name: 'tags'
            text: 'Tags'
            GitcdTagPanel:
                id: tab_panels
    BoxLayout:
        orientation: 'vertical'

        Toolbar:
            title: "Toolbar with left and right buttons"
            pos_hint: {'center_x': 0.5, 'center_y': 0.25}
            md_bg_color: app.theme_cls.bg_light
            specific_text_color: app.theme_cls.text_color
            left_action_items: [['arrow-left', lambda x: None]]
            right_action_items: [['lock', lambda x: None], \
                ['camera', lambda x: None], \
                ['play', lambda x: None]]
        MDLabel:
            color: app.theme_cls.text_color
            text: 'Some text, here is the info panel with actions'
''')


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class GitcdMainPanel(BoxLayout):

    app = None
    branches = []
    tags = []

    def __init__(self, **kwargs):
        super(GitcdMainPanel, self).__init__(**kwargs)
        threading.Thread(target=self.initialize).start()

    def initialize(self, **kwargs):
        pass




# MDTabbedPanel:
#                     id: tab_panel
#                     tab_display_mode:'text'

#                     MDTab:
#                         name: 'music'
#                         text: "Music" # Why are these not set!!!
#                         icon: "playlist-play"
#                         MDLabel:
#                             font_style: 'Body1'
#                             theme_text_color: 'Primary'
#                             text: "Here is my music list :)"
#                             halign: 'center'
#                     MDTab:
#                         name: 'movies'
#                         text: 'Movies'
#                         icon: "movie"

#                         MDLabel:
#                             font_style: 'Body1'
#                             theme_text_color: 'Primary'
#                             text: "Show movies here :)"
#                             halign: 'center'