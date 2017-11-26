import os
import simpcli

import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivymd.theming import ThemeManager

from gitcd.git.exceptions import NoRepositoryException


from pprint import pprint
import inspect

class Kivy(App):
    currentDirectory = StringProperty()
    cli = simpcli.Command()

    theme_cls = ThemeManager()
    theme_cls.theme_style = 'Dark'
    theme_cls.primary_palette = 'LightGreen'
    theme_cls.accent_palette = 'Orange'

    def setCurrentDirectory(self, directory: str):
        if not os.path.exists(directory):
            # error dialog maybe?
            return False

        self.currentDirectory = directory
        os.chdir(self.currentDirectory)

    def getCurrentRepository(self):
        return self.currentRepository

    def build(self):

        pprint(inspect.getmembers(self.theme_cls))
        return Builder.load_string("""
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
#:import GitcdUpgradeDialog gitcd.interface.kivy.upgrade.GitcdUpgradeDialog
#:import GitcdCleanDialog gitcd.interface.kivy.clean.GitcdCleanDialog
#:import GitcdNavigationDrawer gitcd.interface.kivy.navigation.GitcdNavigationDrawer
#:import GitcdBranchPanel gitcd.interface.kivy.branchpanel.GitcdBranchPanel
#:import GitcdTagPanel gitcd.interface.kivy.tagpanel.GitcdTagPanel
#:import GitcdInfoPanel gitcd.interface.kivy.infopanel.GitcdInfoPanel
#:import GitcdMainPanel gitcd.interface.kivy.mainpanel.GitcdMainPanel


NavigationLayout:
    id: nav_layout
    side_panel_width: dp(500)
    GitcdNavigationDrawer:
        id: nav_drawer
    BoxLayout:
        orientation: 'vertical'
        Toolbar:
            id: toolbar
            title: "You are currently in " + app.currentDirectory
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            left_action_items: [['folder-outline', lambda x: app.root.toggle_nav_drawer()]]
            right_action_items: [['sync', lambda x: GitcdCleanDialog().open()], ['help', lambda x: GitcdUpgradeDialog().open()], ['format-color-fill', lambda x: MDThemePicker().open()]]
        BoxLayout:
            spacing: 20
            padding: [20, 20, 20, 20]
            GitcdMainPanel:
                id: main_panel
            # GitcdBranchPanel:
            #     id: branch_panel
            # MDSeparator:
            #     width: dp(1)
            # GitcdTagPanel:
            #     id: tag_panel
            # MDSeparator:
            #     width: dp(1)
            # GitcdInfoPanel:
            #     id: info_panel


""")
