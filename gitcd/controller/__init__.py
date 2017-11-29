from simpcli import CliException

from gitcd.git.repository import Repository
from gitcd.git.remote import Remote


class Base(object):

    repository = Repository()
    config = None
    configPersonal = None
    updateRemotes = False

    def __init__(self):
        self.config = self.repository.getConfig()
        self.configPersonal = self.repository.getPersonalConfig()
        if self.updateRemotes is True:
            self.remoteUpdate()

    def remoteUpdate(self) -> bool:
        remotes = self.repository.getRemotes()

        returnValue = True
        for remote in remotes:
            try:
                remote.update()
            except CliException as e:
                returnValue = False
        return returnValue

    def getRemotes(self) -> [Remote]:
        return self.repository.getRemotes()