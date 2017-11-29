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
        self.branches = []
        self.tags = []
        self.readRemoteConfig()

    def readRemoteConfig(self) -> bool:
        output = self.cli.execute('git config -l')

        if not output:
            return False

        lines = output.split("\n")
        url = False
        for line in lines:
            if line.startswith("remote.%s.url=" % (self.name)):
                lineParts = line.split("=")
                url = lineParts[1]

        # in case of https
        # https://github.com/claudio-walser/test-repo.git
        if url.startswith("https://") or url.startswith("http://"):
            url = url.replace("http://", "")
            url = url.replace("https://", "")
        # in case of ssh git@github.com:claudio-walser/test-repo.git
        else:
            urlParts = url.split("@")
            url = urlParts[1]
            url = url.replace(":", "/")

        self.url = url

        urlParts = url.split("/")
        self.username = urlParts[1]

        return True

    def getName(self) -> str:
        return self.name

    def getUrl(self) -> str:
        return self.url

    def getUsername(self) -> str:
        return self.usernme

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

    def update(self) -> bool:
        self.cli.execute('git remote update %s' % (self.name))

        return True

    def createFeature(self, feature: str) -> Branch:
        self.verboseCli.execute(
            "git checkout %s" % (self.config.getMaster())
        )
        self.verboseCli.execute(
            "git pull %s %s" % (self.name, self.config.getMaster())
        )
        self.verboseCli.execute(
            "git checkout -b %s" % (feature)
        )
        self.verboseCli.execute(
            "git push %s %s" % (self.name, feature)
        )
        self.verboseCli.execute(
            "git branch --set-upstream-to %s/%s" % (self.name, feature)
        )