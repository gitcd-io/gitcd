import os
from typing import List

from gitcd.git import Git
from gitcd.git.branch import Branch
from gitcd.git.remote import Remote
from gitcd.git.tag import Tag

# git exceptions
from gitcd.git.exceptions import NoRepositoryException
from gitcd.git.exceptions import RemoteNotFoundException
from gitcd.git.exceptions import BranchNotFoundException
from gitcd.git.exceptions import TagNotFoundException

# default exceptions
from gitcd.exceptions import GitcdNoDevelopmentBranchDefinedException


class Repository(Git):

    directory = None
    name = None
    remotes = []

    def __init__(self):
        self.directory = self.cli.execute('git rev-parse --show-toplevel')

        if self.directory is False:
            raise NoRepositoryException(
                'No git repository found in %s' % (
                    os.getcwd()
                )
            )

    def getDirectory(self) -> str:
        return self.directory

    def getRemotes(self) -> List[Remote]:
        output = self.cli.execute('git remote')
        if not output:
            return []

        lines = output.split("\n")

        remotes = []
        for line in lines:
            line = line.strip()
            remotes.append(Remote(line))

        return remotes

    def getRemote(self, remoteStr: str) -> Remote:
        remotes = self.getRemotes()
        for remote in remotes:
            if remote.getName() == remoteStr:
                return remote

        raise RemoteNotFoundException('Remote %s not found' % (remoteStr))

    def getBranches(self) -> List[Branch]:
        output = self.cli.execute('git branch -a')
        if not output:
            return []

        lines = output.split("\n")
        branches = []
        for line in lines:
            line = line.strip()
            if 'HEAD -> ' in line:
                continue

            if not line.startswith('remotes/'):
                branch = line.replace('* ', '')
            elif line.startswith('remotes/'):
                parts = line.split('/')
                del parts[0]
                del parts[0]
                branch = '/'.join(parts)
            if branch not in branches:
                branches.append(branch)

        branchObjects = []
        branches.sort()
        for branch in branches:
            branchObject = Branch(branch)
            branchObjects.append(branchObject)

        return branchObjects

    def getDevelopmentBranches(self) -> [Branch]:
        branches = self.getBranches()
        developmentBranches = []
        for branch in branches:
            if branch.isTest():
                developmentBranches.append(branch)

        if len(developmentBranches) < 1:
            raise GitcdNoDevelopmentBranchDefinedException(
                "No development branch found"
            )
        return developmentBranches

    def getBranch(self, branchStr: str) -> Branch:
        branches = self.getBranches()
        for branch in branches:
            if branch.getName() == branchStr:
                return branch

        raise BranchNotFoundException('Branch %s not found' % (branchStr))

    def getCurrentBranch(self) -> Branch:
        return Branch(self.cli.execute('git rev-parse --abbrev-ref HEAD'))

    def checkoutBranch(self, branch: Branch) -> Branch:
        self.verboseCli.execute('git checkout %s' % (branch.getName()))
        return branch

    def getTags(self) -> List[Tag]:
        output = self.cli.execute('git tag -l')
        if not output:
            return []

        lines = output.split("\n")

        tags = []
        for line in lines:
            tag = line.strip()

            if tag not in tags:
                tags.append(tag)

        tagObjects = []
        tags.sort()
        for tag in tags:
            tagObject = Tag(tag)
            tagObjects.append(tagObject)

        return tagObjects

    def getTag(self, tagStr: str) -> Tag:
        tags = self.getTags()
        for tag in tags:
            if tag.getName() == tagStr:
                return tag

        raise TagNotFoundException('Tag %s not found' % (tagStr))

    def getLatestTag(self) -> [Branch, Tag]:
        output = self.cli.execute("git describe --abbrev=0")
        if not output:
            return Branch(self.config.getMaster())
        return Tag(output.strip())

    def hasUncommitedChanges(self) -> bool:
        output = self.cli.execute("git status --porcelain")
        if not output:
            return False

        return True

    def stash(self) -> bool:
        self.verboseCli.execute("git stash")
        return True

    def stashPop(self) -> bool:
        self.verboseCli.execute("git stash pop")
        return True

    def update(self) -> bool:
        self.cli.execute('git fetch -p')

        return True
