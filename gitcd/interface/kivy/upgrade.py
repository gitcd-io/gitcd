from packaging import version
import threading

from kivy.lang import Builder
from kivy.clock import Clock

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView

from kivymd.label import MDLabel

from gitcd.package import Package


Builder.load_string('''
#:import MDSpinner kivymd.spinner.MDSpinner

<GitcdUpgradeDialog>:
    size_hint: (None, None)
    size: dp(284), dp(80)+dp(290)

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
        text: "Upgrade"
        size_hint: (None, None)
        size: dp(100), dp(50)
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        theme_text_color: 'Custom'

    MDSpinner:
        id: spinner
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        active: True

    MDRaisedButton:
        id: buttonUpgrade
        pos: root.pos[0] + dp(10), root.pos[1] + dp(10)
        text: "Upgrade"
        on_release: root.upgrade()
        disabled: True
    MDRaisedButton:
        pos: root.pos[0]+root.size[0]-self.width-dp(10), root.pos[1] + dp(10)
        text: "Close"
        on_release: root.dismiss()
''')

class GitcdUpgradeDialog(FloatLayout, ModalView):

    package = Package()

    def open(self, **kwargs):
        super(GitcdUpgradeDialog, self).open(**kwargs)
        threading.Thread(target=self.loadVersions).start()

    def loadVersions(self):
        localVersion = self.package.getLocalVersion()

        try:
            pypiVersion = self.package.getPypiVersion()
        except GitcdPyPiApiException as e:
            pypiVersion = 'unknown'

        versionText = 'Local Version: %s' % localVersion
        versionText += '\nPyPI Version: %s' % pypiVersion

        label = MDLabel(
            text = versionText,
            theme_text_color = 'Primary',
            size_hint = [None, None],
            size = [244, 40],
            pos_hint = {'center_x': 0.5, 'center_y': 0.65}
        )

        self.remove_widget(self.ids.spinner)
        self.add_widget(label)

        if version.parse(localVersion) < version.parse(pypiVersion):
            self.ids.buttonUpgrade.disabled = False

    def upgrade(self):
        self.package.upgrade()
        