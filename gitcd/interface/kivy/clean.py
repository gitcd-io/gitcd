import threading

from kivy.lang import Builder

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView



from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.button import MDIconButton


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
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint: (None, None)
        size: dp(344), dp(200)

        MDList:
            id: ml
            OneLineIconListItem:
                text: "test-branch"
                disabled: True
                IconLeftSampleWidget:
                    icon: 'source-branch'
            OneLineIconListItem:
                text: "test-branch-3"
                disabled: True
                IconLeftSampleWidget:
                    icon: 'source-branch'
            OneLineIconListItem:
                text: "test-branch-2"
                disabled: True
                IconLeftSampleWidget:
                    icon: 'source-branch'
            OneLineIconListItem:
                text: "v0.0.2"
                disabled: True
                IconLeftSampleWidget:
                    icon: 'tag'
            OneLineIconListItem:
                text: "v0.0.3"
                disabled: True
                IconLeftSampleWidget:
                    icon: 'tag'
            OneLineIconListItem:
                text: "v0.0.4"
                disabled: True
                IconLeftSampleWidget:
                    icon: 'tag'




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

class GitcdCleanDialog(FloatLayout, ModalView):


    def open(self, **kwargs):
        super(GitcdCleanDialog, self).open(**kwargs)
        threading.Thread(target=self.loadBranches).start()

    def loadBranches(self):
        self.remove_widget(self.ids.spinner)
        
        self.ids.buttonClean.disabled = False

        #self.add_widget(label)

        # if version.parse(localVersion) < version.parse(pypiVersion):
        #     self.ids.buttonUpgrade.disabled = False

    def clean(self):
        pass
    
class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass