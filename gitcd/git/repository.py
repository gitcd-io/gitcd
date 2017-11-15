from typing import List

from gitcd.git import Git

from gitcd.git.branch import Branch
from gitcd.git.remote import Remote
from gitcd.git.tag import Tag

class Repository(Git):

    def getName(self) -> str:
        pass

    def getRemotes(self) -> List[Remote]:
        pass

    def getRemote(self) -> Remote:
        pass

    def getBranches(self) -> List[Branch]:
        pass

    def getBranch(self) -> Branch:
        pass

    def getTags(self) -> List[Tag]:
        pass

    def getTag(self) -> Tag:
        pass