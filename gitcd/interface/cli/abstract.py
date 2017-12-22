import os
import simpcli

from gitcd.git.repository import Repository
from gitcd.git.branch import Branch

from gitcd.config import Gitcd as GitcdConfig
from gitcd.config import GitcdPersonal as GitcdPersonalConfig

from gitcd.controller import Base as BaseController


class BaseCommand(object):

    interface = simpcli.Interface()
    config = GitcdConfig()
    configPersonal = GitcdPersonalConfig()

    def run(self, branch: Branch):
        pass

    def getRemote(self) -> str:
        base = BaseController()
        remotes = base.getRemotes()

        if len(remotes) == 1:
            remote = remotes[0]
        else:
            if len(remotes) == 0:
                default = False
                choice = False
            else:
                default = remotes[0].getName()
                choice = []
                for remoteObj in remotes:
                    choice.append(remoteObj.getName())

            remoteAnswer = self.interface.askFor(
                "Which remote you want to use?",
                choice,
                default
            )
            for remoteObj in remotes:
                if remoteAnswer == remoteObj.getName():
                    remote = remoteObj

        return remote