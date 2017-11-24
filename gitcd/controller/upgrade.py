from packaging import version
import pip
import pkg_resources
import requests

from gitcd.controller import Base

from gitcd.git.repository import Repository

from gitcd.exceptions import GitcdPyPiApiException


class Upgrade(Base):

    localVersion = 0
    pypiVersion = 0
    packageUrl = 'https://pypi.org/pypi/gitcd/json'

    def getLocalVersion(self) -> str:
        self.localVersion = pkg_resources.get_distribution("gitcd").version

        return self.localVersion

    def getPypiVersion(self) -> str:
        response = requests.get(
            self.packageUrl
        )

        if response.status_code != 200:
            raise GitcdPyPiApiException(
                "Could not fetch version info on PyPi site." +
                "You need to check manually, sorry for that."
            )

        result = response.json()
        self.pypiVersion = result['info']['version']

        return self.pypiVersion

    def isUpgradable(self) -> bool:
        if version.parse(self.localVersion) < version.parse(self.pypiVersion):
            return True
        return False

    def upgrade(self) -> bool:
        pip.main(['install', '--user', '--upgrade', 'gitcd'])

        return True
