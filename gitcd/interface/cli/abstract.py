import os
import simpcli

from gitcd.git.repository import Repository

from gitcd.config import Gitcd as GitcdConfig
from gitcd.config import GitcdPersonal as GitcdPersonalConfig


class BaseCommand(object):

    cli = simpcli.Interface()
    config = GitcdConfig()
    configPersonal = GitcdPersonalConfig()

    def run(self, branch: str):
        pass
