from gitcd.config import Gitcd as GitcdConfig
from gitcd.config import GitcdPersonal as GitcdPersonalConfig


class App(object):
    config = GitcdConfig()
    configPersonal = GitcdPersonalConfig()
