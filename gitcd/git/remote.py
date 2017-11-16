from typing import List

from gitcd.git import Git

from gitcd.git.branch import Branch
from gitcd.git.tag import Tag


class Remote(Git):

    name = 'origin'

    def __init__(self, name: str):
        self.name = name

    def getName(self) -> str:
        pass

    def getUrl(self) -> str:
        pass

    def getUsername(self) -> str:
        pass

    def hasBranch(self, branch: Branch) -> bool:
        pass

    def hasTag(self, tag: Tag) -> bool:
        pass