# flake8: noqa
import threading

import kivy
from kivy.lang import Builder

from gitcd.interface.kivy.panel import GitcdInlineNavigationPanel


Builder.load_string('''
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationDrawerIconButton kivymd.navigationdrawer.NavigationDrawerIconButton

<GitcdBranchPanel>:
    do_scroll_x: False
    id: branch_panel
    MDNavigationDrawer:
        id: branch_list
        NavigationDrawerIconButton:
            text: "test-branch-1"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-2"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-3"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-4"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-5"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-6"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-7"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-8"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-9"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-10"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-11"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-12"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-13"
            icon: 'source-branch'
            on_release: root.onRelease
        NavigationDrawerIconButton:
            text: "test-branch-14"
            icon: 'source-branch'
            on_release: root.onRelease

''')


class GitcdBranchPanel(GitcdInlineNavigationPanel):

    def onRelease(self, **kwargs):
        pass
