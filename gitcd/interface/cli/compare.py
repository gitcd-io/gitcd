from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.repository import Repository

from gitcd.git.branch import Branch
from gitcd.git.tag import Tag


class Compare(BaseCommand):

    def getDefaultBranch(self) -> [Branch, Tag]:
        repository = Repository()
        return repository.getLatestTag()

    def getRequestedBranch(self, branch: str) -> [Branch, Tag]:
        tagPrefix = self.config.getTag()
        if branch.startswith(tagPrefix):
            branch = Tag(branch)
        else:
            branch = Branch(branch)

        return branch

    def run(self, branch: [Branch, Tag]):
        remote = self.getRemote()
        repository = Repository()
        currentBranch = repository.getCurrentBranch()
        self.checkRepository()

        remote.compare(currentBranch, branch)
