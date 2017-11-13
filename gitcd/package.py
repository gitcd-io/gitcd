import pkg_resources
import requests
import pip
from gitcd.exceptions import GitcdPyPiApiException


class Package(object):

    packageUrl = 'https://pypi.org/pypi/gitcd/json'

    def upgrade(self):
    	pip.main(['install', '--user', '--upgrade', 'gitcd'])

    def getLocalVersion(self):
        return pkg_resources.get_distribution("gitcd").version

    def getPypiVersion(self):
        response = requests.get(
            self.packageUrl
        )

        if response.status_code != 200:
            raise GitcdPyPiApiException(
                "Could not fetch version info on PyPi site." +
                "You need to check manually, sorry for that."
            )

        result = response.json()
        return result['info']['version']
