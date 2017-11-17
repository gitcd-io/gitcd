from typing import List

from gitcd.git import Git

from gitcd.git.branch import Branch
from gitcd.git.tag import Tag


class Remote(Git):

    name = 'origin'
    branches = []
    tags = []

    def __init__(self, name: str):
        self.name = name

    def getName(self) -> str:
        return self.name

    def getUrl(self) -> str:
        pass

    def getUsername(self) -> str:
        pass

    def readBranches(self) -> bool:
        if self.branches:
            return True

        output = self.cli.execute('git branch -r')
        if not output:
            return False

        lines = output.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith('%s/' % (self.name)):
                self.branches.append(line.replace('%s/' % (self.name), ''))

        return True

    def readTags(self) -> bool:
        if self.tags:
            return True

        output = self.cli.execute('git ls-remote -t --refs %s' % self.name)
        if not output:
            return False

        lines = output.split("\n")
        for line in lines:
            line = line.strip()
            parts = line.split('refs/tags/')
            self.tags.append(parts[-1])

        return True

    def hasBranch(self, branch: Branch) -> bool:
        self.readBranches()
        if branch.getName() in self.branches:
            return True

        return False

    def hasTag(self, tag: Tag) -> bool:
        self.readTags()
        if tag.getName() in self.tags:
            return True

        return False