from packaging import version

from gitcd.interface.cli.abstract import BaseCommand
from gitcd.package import Package

from gitcd.exceptions import GitcdPyPiApiException


class Upgrade(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd upgrade')

        package = Package()
        localVersion = package.getLocalVersion()

        try:
            pypiVersion = package.getPypiVersion()
        except GitcdPyPiApiException as e:
            pypiVersion = 'unknown'
            message = str(e)

        self.cli.info('Local %s' % localVersion)
        self.cli.info('PyPi %s' % pypiVersion)

        if pypiVersion == 'unknown':
            self.cli.error(message)
            return False

        if version.parse(localVersion) < version.parse(pypiVersion):
            upgrade = self.cli.askFor(
                "Do you want me to upgrade gitcd for you?",
                ["yes", "no"],
                "yes"
            )
            if upgrade == 'yes':
                try:
                    package.upgrade()
                    return True
                except SystemExit as e:
                    self.cli.error('An error occured during the update!')
                    pass

            self.cli.info(
                'Please upgrade by running pip3 install --user --upgrade gitcd'
            )
            return False
        else:
            self.cli.ok(
                'You seem to be on the most recent version, congratulation!'
            )
            return True
