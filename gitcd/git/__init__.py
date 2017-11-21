import simpcli

from gitcd.config import Gitcd as GitcdConfig
from gitcd.config import GitcdPersonal as GitcdPersonalConfig


class Git(object):

    cli = simpcli.Command()
    verboseCli = simpcli.Command(True)
    config = GitcdConfig()
    configPersonal = GitcdPersonalConfig()

    def getConfig(self) -> GitcdConfig:
        return self.config

    def getPersonalConfig(self) -> GitcdPersonalConfig:
        return self.configPersonal
