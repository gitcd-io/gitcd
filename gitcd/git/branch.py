from gitcd.git import Git

class Branch(Git):

    def getName(self) -> str:
        pass

    def hasUncommitedChanges(self) -> bool:
        pass

    def isBehindRemote(self) -> bool:
        pass

    def isRemote(self) -> bool:
        pass

    def isLocal(self) -> bool:
        pass

