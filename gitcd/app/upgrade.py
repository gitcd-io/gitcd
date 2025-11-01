import simpcli
from packaging import version as parse_version
from importlib.metadata import version
import requests

from gitcd.app import App

from gitcd.exceptions import GitcdPyPiApiException


class Upgrade(App):

    localVersion: str = ""
    pypiVersion: str = ""
    packageUrl = 'https://pypi.org/pypi/gitcd/json'
    verboseCli = simpcli.Command(True)

    def getLocalVersion(self) -> str:
        self.localVersion = version("gitcd")

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
        if parse_version.parse(self.localVersion) < parse_version.parse(self.pypiVersion):
            return True
        return False

    def upgrade(self) -> bool:
        self.verboseCli.execute("pip3 install --user --upgrade gitcd")

        return True
