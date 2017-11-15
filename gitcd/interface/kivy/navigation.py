import threading

import kivy
from kivy.lang import Builder
from kivymd.navigationdrawer import MDNavigationDrawer
from kivymd.navigationdrawer import NavigationDrawerIconButton

import simpcli

Builder.load_string('''
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar

<GitcdNavigationDrawer>:
    id: nav_drawer
    NavigationDrawerToolbar:
        title: "Your repositories"
        #right_action_items: [['folder-plus', lambda x: app.root.toggle_nav_drawer()]]
        left_action_items: [['close', lambda x: app.root.toggle_nav_drawer()]]
''')

class GitcdNavigationDrawer(MDNavigationDrawer):

    app = None

    def __init__(self, **kwargs):
        super(GitcdNavigationDrawer, self).__init__(**kwargs)
        threading.Thread(target=self.initialize).start()

    def readGitCdFolders(self):
        cli = simpcli.Command()
        result = cli.execute('find ~ -path "*/.gitcd" 2>/dev/null', True)
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

