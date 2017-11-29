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
        testPrefix = self.config.getTest()
        if not testPrefix:
            return False

        return self.name.startswith(testPrefix)

    def isFeature(self) -> bool:
        if self.isMaster() or self.isTest():
            return False

        if self.config.getFeature():
            return self.name.startswith(self.config.getFeature())
        return True

    def delete(self) -> bool:
        output = self.verboseCli.execute("git branch -D %s" % (self.name))
        if output is False:
            return False
        return True
