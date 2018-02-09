from gitcd.interface.cli.abstract import BaseCommand

from gitcd.app.upgrade import Upgrade as UpgradeHelper

from gitcd.git.branch import Branch

from gitcd.exceptions import GitcdPyPiApiException


class Upgrade(BaseCommand):

    def run(self, branch: Branch):
        helper = UpgradeHelper()

        localVersion = helper.getLocalVersion()

        try:
            pypiVersion = helper.getPypiVersion()
        except GitcdPyPiApiException as e:
            pypiVersion = 'unknown'
            message = str(e)

        self.interface.info('Local %s' % localVersion)
        self.interface.info('PyPi %s' % pypiVersion)

        if pypiVersion == 'unknown':
            self.interface.error(message)
            return False

        if helper.isUpgradable():
            upgrade = self.interface.askFor(
                "Do you want me to upgrade gitcd for you?",
                ["yes", "no"],
                "yes"
            )
            if upgrade == 'yes':
                try:
                    helper.upgrade()
                    return True
                except SystemExit as e:
                    self.interface.error('An error occured during the update!')
                    pass

            self.interface.info(
                'Please upgrade by running pip3 install --user --upgrade gitcd'
            )
            return False
        else:
            self.interface.ok(
                'You seem to be on the most recent version, congratulation!'
            )
            return True

    # dont need a real repository for upgrading
    def instantiateRepository(self) -> bool:
        return True

    def getDefaultBranch(self) -> Branch:
        return False

    def getRequestedBranch(self, branch: str) -> Branch:
        return False
