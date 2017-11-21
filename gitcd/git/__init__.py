import simpcli

from gitcd.config import Gitcd as GitcdConfig
from gitcd.config import GitcdPersonal as GitcdPersonalConfig


class Git(object):

    cli = simpcli.Command()
    verboseCli = simpcli.Command(True)
    config = GitcdConfig()
    configPersonal = GitcdPersonalConfig()
