from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.branch import Branch
from gitcd.app.upgrade import Upgrade as UpgradeHelper


class Version(BaseCommand):

    updateRemote = True

    def run(self, branch: Branch):
        helper = UpgradeHelper()

        localVersion = helper.getLocalVersion()

        self.interface.info(
            'You run git-cd in version %s' % (localVersion)
        )
