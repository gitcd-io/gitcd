import os
from typing import List

from gitcd.git import Git

from gitcd.git.branch import Branch
from gitcd.git.remote import Remote
from gitcd.git.tag import Tag

from gitcd.exceptions import GitcdNoRepositoryException

from pprint import pprint

class Repository(Git):

    directory = None
    name = None
    remotes = []

    def __init__(self, repositoryDirectory: str):
        self.directory = repositoryDirectory


        # self.setCwd()
        # output = self.cli.execute('git remote -v')
        # lines = output.split('\n')
        # for line in lines:
        #     lineParts = line.split('\t')
        #     if lineParts[1].endswith('(push)'):
        #         self.remotes.append({
        #             'name': lineParts[0],
        #             'url': lineParts[1].replace(' (push)', '')
        #         })

    def setCwd(self) -> bool:
        try:
            os.chdir(self.directory)
            if not os.path.exists('%s/.git' % (self.directory)):
                raise Exception('no git')
        except Exception:
            raise GitcdNoRepositoryException(
                'No git repository found in %s' % (
                    self.directory
                )
            )
        return True

    # def getName(self) -> str:
    #     pass

    def getRemotes(self) -> List[Remote]:
        self.setCwd()
        output = self.cli.execute('git remote')
        if not output:
            self.interface.error(
                "An error occured while reading remotes." +
                " Please pass it manually!"
            )
            return []

        lines = output.split("\n")

        remotes = []
        for line in lines:
            remotes.append(Remote(line))

        return remotes
        # pass

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