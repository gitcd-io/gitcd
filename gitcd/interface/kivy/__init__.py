import simpcli
import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty

from kivymd.theming import ThemeManager
from kivymd.navigationdrawer import MDNavigationDrawer
from kivymd.navigationdrawer import NavigationDrawerIconButton

from gitcd.interface.kivy.upgrade import GitcdUpgradeDialog



from pprint import pprint

class GitcdNavigationDrawer(MDNavigationDrawer):

    app = None

    def __init__(self, **kwargs):
        super(GitcdNavigationDrawer, self).__init__(**kwargs)

    def readGitCdFolders(self):
        #find ~ -path "*/.git" -a -type d 2>/dev/null
        cli = simpcli.Command()
        result = cli.execute('find ~ -path "*/.gitcd" 2>/dev/null', 1)
        folders = result.split("\n")
        gitFolders = []
        for folder in folders:
            folder = folder.replace('/.gitcd', '')
            folderParts = folder.split('/')
            gitFolder = {
                'name': folderParts[-1],
                'path': folder
            }
            gitFolders.append(gitFolder)
        return gitFolders

    def initialize(self):
        print('wtf')
        self.app = kivy.app.App.get_running_app()

        gitFolders = self.readGitCdFolders()

        for folder in gitFolders:
            button = NavigationDrawerIconButton(
                text = folder['name'],
                on_release = self.onRelease
            )
            button.icon = 'github-circle'
            button.path = folder['path']
            self.add_widget(button)

    def onRelease(self, button):
        self.app.setCurrentRepository(button.path)


class Kivy(App):
    currentRepository = StringProperty()
    cli = simpcli.Command()

    theme_cls = ThemeManager()
    theme_cls.theme_style = 'Dark'
    theme_cls.primary_palette = 'LightGreen'
    theme_cls.accent_palette = 'Orange'
    
    def setCurrentRepository(self, currentRepository: str):
        self.currentRepository = currentRepository
        print(self.currentRepository)
    
    def getCurrentRepository(self):
        return self.currentRepository
    
    def build(self):
        main_widget = Builder.load_string("""
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import MDThemePicker kivymd.theme_picker.MDThemePicker


NavigationLayout:
    id: nav_layout
    side_panel_width: dp(500)
    GitcdNavigationDrawer:
        id: nav_drawer
        width: dp(1010)
        NavigationDrawerToolbar:
            title: "Your repositories"
            #right_action_items: [['folder-plus', lambda x: app.root.toggle_nav_drawer()]]
            left_action_items: [['close', lambda x: app.root.toggle_nav_drawer()]]
    BoxLayout:
        orientation: 'vertical'
        Toolbar:
            id: toolbar
            title: "You are currently in " + app.currentRepository
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            left_action_items: [['folder-outline', lambda x: app.root.toggle_nav_drawer()]]
            right_action_items: [['help', lambda x: app.showVersion()], ['format-color-fill', lambda x: MDThemePicker().open()]]
        MDLabel:
            text: "Current: " + app.currentRepository
            theme_text_color: 'Primary'
            pos_hint: {'center_x': 0.5}
            halign: 'center'
""")
        main_widget.ids.nav_drawer.initialize()
        #self.root.ids.nav_drawer.initialize()
        return main_widget



    def showVersion(self):
        GitcdUpgradeDialog().open()
