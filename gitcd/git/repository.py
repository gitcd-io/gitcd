import os
from typing import List

from gitcd.git import Git
from gitcd.git.branch import Branch
from gitcd.git.remote import Remote
from gitcd.git.tag import Tag

from gitcd.git.exceptions import NoRepositoryException
from gitcd.git.exceptions import RemoteNotFoundException
from gitcd.git.exceptions import BranchNotFoundException
from gitcd.git.exceptions import TagNotFoundException


class Repository(Git):

    directory = None
    name = None
    remotes = []

    def __init__(self, repositoryDirectory: str):
        self.directory = repositoryDirectory
        self.setCwd()

    def getDirectory(self) -> str:
        return self.directory

    def setCwd(self) -> bool:
        try:
            os.chdir(self.directory)
            if not os.path.exists('%s/.git' % (self.directory)):
                raise Exception('no git')
        except Exception:
            raise NoRepositoryException(
                'No git repository found in %s' % (
                    self.directory
                )
            )
        return True

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
        branchObjects = []
        for line in lines:
            line = line.strip()
            if not line.startswith("remotes/"):
                branch = line.replace("* ", "")
            else:
                lineParts = line.split('/')
                branch = lineParts[-1]
            branchObject = Branch(branch)
            if branch not in branches:
                branches.append(branch)
                branchObjects.append(branchObject)

        return branchObjects

    def getBranch(self, branchStr: str) -> Branch:
        branches = self.getBranches()
        for branch in branches:
            if branch.getName() == branchStr:
                return branch

        raise BranchNotFoundException('Branch %s not found' % (branchStr))

    def getCurrentBranch(self) -> Branch:
        return Branch(self.cli.execute('git rev-parse --abbrev-ref HEAD'))
        
    def checkoutBranch(self, branchStr: str) -> Branch:
        self.verboseCli.execute('git checkout %s' % (branchStr))
        return self.getCurrentBranch()

    def getTags(self) -> List[Tag]:
        output = self.cli.execute('git tag -l')
        if not output:
            return []

        lines = output.split("\n")

        tags = []
        tagObjects = []
        for line in lines:
            tag = line.strip()

            tagObject = Tag(tag)
            if tag not in tags:
                tags.append(tag)
                tagObjects.append(tagObject)

        return tagObjects

    def getTag(self, tagStr: str) -> Tag:
        tags = self.getTags()
        for tag in tags:
            if tag.getName() == tagStr:
                return tag

        raise TagNotFoundException('Tag %s not found' % (tagStr))
