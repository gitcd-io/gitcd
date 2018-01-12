from typing import Union

from gitcd.git import Git
from gitcd.git.pullRequest import Github
from gitcd.git.pullRequest import Bitbucket
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
        self.repositoryName = urlParts[-1]
        self.repositoryName = self.repositoryName.replace('.git', '')

        return True

    def getName(self) -> str:
        return self.name

    def getRepositoryName(self) -> str:
        return self.repositoryName

    def getUrl(self) -> str:
        return self.url

    def getUsername(self) -> str:
        return self.username

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
        self.cli.execute('git remote update -p %s' % (self.name))

        return True

    def push(self, branch: Union[Branch, Tag]) -> bool:
        self.verboseCli.execute(
            "git push %s %s" % (self.name, branch.getName())
        )
        if type(branch) is Branch:
            self.verboseCli.execute(
                "git branch --set-upstream-to %s/%s" % (
                    self.name,
                    branch.getName()
                )
            )
        return True

    def pull(self, branch: Branch) -> bool:
        self.verboseCli.execute(
            'git pull %s %s' % (self.name, branch.getName())
        )
        return True

    def delete(self, branch: Branch) -> bool:
        output = self.verboseCli.execute("git push %s :%s" % (
            self.name, branch.getName())
        )
        if output is False:
            return False
        return True

    def isBehind(self, branch: Branch) -> bool:
        output = self.cli.execute(
            "git log %s/%s..%s" % (
                self.name,
                branch.getName(),
                branch.getName()
            )
        )
        if not output:
            return False

        return True

    def createFeature(self, branch: Branch) -> Branch:
        self.verboseCli.execute(
            "git checkout %s" % (self.config.getMaster())
        )
        self.verboseCli.execute(
            "git pull %s %s" % (self.name, self.config.getMaster())
        )
        self.verboseCli.execute(
            "git checkout -b %s" % (branch.getName())
        )

        self.push(branch)

        return branch

    def merge(self, branch: Branch, branchToMerge: Branch) -> bool:
        self.verboseCli.execute("git checkout %s" % (branch.getName()))
        self.verboseCli.execute("git pull %s %s" % (
            self.name,
            branch.getName()
        ))
        self.verboseCli.execute("git merge %s/%s" % (
            self.name,
            branchToMerge.getName()
        ))
        self.push(branch)

    def compare(self, branch: Branch, toCompare: [Branch, Tag]) -> bool:
        if isinstance(toCompare, Tag):
            toCompareString = toCompare.getName()
        else:
            toCompareString = '%s/%s' % (self.name, toCompare.getName())
        self.verboseCli.execute("git diff %s %s --color" % (
            toCompareString,
            branch.getName()
        ))
        return True

    # @todo: method for getting pr instance instead of reimplement
    def openPullRequest(
        self,
        title: str,
        body: str,
        fromBranch: Branch,
        toBranch: Branch
    ) -> bool:
        if self.isGithub():
            pr = Github()
        elif self.isBitbucket():
            pr = Bitbucket()
        else:
            # todo: raise RepoProviderNotImplementedException
            return False

        pr.setRemote(self)
        pr.open(title, body, fromBranch, toBranch)

    # @todo: method for getting pr instance instead of reimplement
    def statusPullRequest(self, branch: Branch) -> bool:
        if self.isGithub():
            pr = Github()
        elif self.isBitbucket():
            pr = Bitbucket()
        else:
            # todo: raise RepoProviderNotImplementedException
            return False

        pr.setRemote(self)
        return pr.status(branch)

    def isGithub(self) -> bool:
        return 'github.com' in self.url

    def isBitbucket(self) -> bool:
        return 'bitbucket.org' in self.url
