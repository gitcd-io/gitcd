# flake8: noqa
import threading

import kivy
from kivy.lang import Builder

from gitcd.interface.kivy.panel import GitcdInlineNavigationPanel


Builder.load_string('''
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationDrawerIconButton kivymd.navigationdrawer.NavigationDrawerIconButton

<GitcdTagPanel>:
    do_scroll_x: False
    id: branch_panel
    MDNavigationDrawer:
        id: branch_list
        NavigationDrawerIconButton:
            text: "v0.0.1"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.2"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.3"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.4"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.5"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.6"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.7"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.8"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.9"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.10"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.11"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.12"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.13"
            icon: 'tag'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "v0.0.14"
            icon: 'tag'
            on_release: root.onRelease

''')


class GitcdTagPanel(GitcdInlineNavigationPanel):

    def onRelease(self, **kwargs):
        pass
