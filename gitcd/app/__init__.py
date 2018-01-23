from gitcd.config import Gitcd as GitcdConfig
from gitcd.config import GitcdPersonal as GitcdPersonalConfig
from gitcd.git.repository import Repository


class App(object):
    config = GitcdConfig()
    configPersonal = GitcdPersonalConfig()
    repository = Repository()
