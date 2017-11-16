from gitcd.git import Git

class Branch(Git):

    def getName(self) -> str:
        pass

    def hasUncommitedChanges(self) -> bool:
        pass

    def isBehindRemote(self) -> bool:
        pass

    def isMaster(self) -> bool:
        pass

    def isTest(self) -> bool:
        pass

    def isFeature(self) -> bool:
        pass

    def getName(self) -> str:
        pass

    def delete(self) -> bool:
        pass
