import threading

import kivy
from kivy.lang import Builder

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView

from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem, OneLineIconListItem
from kivymd.button import MDIconButton

from gitcd.controller.clean import Clean as CleanController

from pprint import pprint

import time

Builder.load_string('''
#:import MDSpinner kivymd.spinner.MDSpinner

<GitcdCleanDialog>:
    size_hint: (None, None)
    size: dp(384), dp(80)+dp(290)

    canvas:
        Color:
            rgb: app.theme_cls.primary_color
        Rectangle:
            size: self.width, dp(80)
            pos: root.pos[0], root.pos[1] + root.height-dp(80)
        Color:
            rgb: app.theme_cls.bg_normal
        Rectangle:
            size: self.width, dp(290)
            pos: root.pos[0], root.pos[1] + root.height-(dp(80)+dp(290))

    MDLabel:
        font_style: "Headline"
        text: "Clean"
        size_hint: (None, None)
        size: dp(80), dp(50)
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        theme_text_color: 'Custom'

    MDSpinner:
        id: spinner
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        active: True

    ScrollView:
        do_scroll_x: False
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint: (None, None)
        size: dp(344), dp(200)

        MDList:
            id: list

    MDRaisedButton:
        id: buttonClean
        pos: root.pos[0] + dp(10), root.pos[1] + dp(10)
        text: "Clean"
        on_release: root.clean()
        disabled: True
    MDRaisedButton:
        pos: root.pos[0]+root.size[0]-self.width-dp(10), root.pos[1] + dp(10)
        text: "Close"
        on_release: root.dismiss()
''')


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class GitcdCleanDialog(FloatLayout, ModalView):

    app = None
    controller = None
    branches = []
    tags = []

    def open(self, **kwargs):
        super(GitcdCleanDialog, self).open(**kwargs)
        self.app = kivy.app.App.get_running_app()
        self.branches = []
        self.tags = []

        threading.Thread(target=self.loadBranches).start()

    def loadBranches(self):
        self.controller = CleanController()

        self.branches = self.controller.getBranchesToDelete()
        self.tags = self.controller.getTagsToDelete()

        pprint(self.tags)
        pprint(self.branches)
        self.remove_widget(self.ids.spinner)

        for branch in self.branches:
            item = OneLineIconListItem(
                text=branch.getName(),
                disabled=True
            )
            item.add_widget(IconLeftSampleWidget(
                icon='source-branch'
            ))
            self.ids.list.add_widget(item)
            time.sleep(0.2)

        for tag in self.tags:
            item = OneLineIconListItem(
                text=tag.getName(),
                disabled=True
            )
            item.add_widget(IconLeftSampleWidget(
                icon='tag'
            ))
            self.ids.list.add_widget(item)
            time.sleep(0.2)

        if len(self.branches) > 0 or len(self.tags) > 0:
            self.ids.buttonClean.disabled = False

    def clean(self):
        self.controller.deleteBranches(self.branches)
        self.controller.deleteTags(self.tags)
        self.dismiss()
