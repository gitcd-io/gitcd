from gitcd.git import Git

from pprint import pprint

class Branch(Git):

    name = 'master'

    def __init__(self, name: str):
        self.name = name

    def getName(self) -> str:
        return self.name

    def hasUncommitedChanges(self) -> bool:
        pass

    def isBehindRemote(self) -> bool:
        pass

    def isMaster(self) -> bool:
        return self.name == self.config.getMaster()

    def isTest(self) -> bool:
        pass

    def isFeature(self) -> bool:
        pass

    def delete(self) -> bool:
        output = self.verboseCli.execute("git branch -D %s" % (self.name))
        if output is False:
            return False
        return True
