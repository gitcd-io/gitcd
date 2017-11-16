from typing import List

from gitcd.git import Git

from gitcd.git.branch import Branch
from gitcd.git.tag import Tag


class Remote(Git):

    def getName(self) -> str:
        pass

    def getUrl(self) -> str:
        pass

    def getUsername(self) -> str:
        pass

    def getBranches(self) -> List[Branch]:
        pass

    def getBranch(self) -> Branch:
        pass

    def getTags(self) -> List[Tag]:
        pass

    def getTag(self) -> Tag:
        pass