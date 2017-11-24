import threading

import kivy
from kivy.lang import Builder

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
''')


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class GitcdMainPanel(MDTabbedPanel):

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