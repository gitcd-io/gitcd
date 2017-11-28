from gitcd.interface.cli.abstract import BaseCommand

from gitcd.controller.upgrade import Upgrade as UpgradeController

from gitcd.exceptions import GitcdPyPiApiException


class Upgrade(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd upgrade')

        controller = UpgradeController()

        localVersion = controller.getLocalVersion()

        try:
            pypiVersion = controller.getPypiVersion()
        except GitcdPyPiApiException as e:
            pypiVersion = 'unknown'
            message = str(e)

        self.interface.info('Local %s' % localVersion)
        self.interface.info('PyPi %s' % pypiVersion)

        if pypiVersion == 'unknown':
            self.interface.error(message)
            return False

        if controller.isUpgradable():
            upgrade = self.interface.askFor(
                "Do you want me to upgrade gitcd for you?",
                ["yes", "no"],
                "yes"
            )
            if upgrade == 'yes':
                try:
                    controller.upgrade()
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
