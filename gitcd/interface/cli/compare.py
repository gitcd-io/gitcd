from gitcd.interface.cli.abstract import BaseCommand

from gitcd.controller.compare import Compare as CompareController

from gitcd.git.branch import Branch
from gitcd.git.tag import Tag


class Compare(BaseCommand):

    def getDefaultBranch(self) -> [Branch, Tag]:
        controller= CompareController()
        repository = controller.getRepository()
        return repository.getLatestTag()

    def getRequestedBranch(self, branch: str) -> [Branch, Tag]:
        masterBranch = self.config.getMaster()
        tagPrefix = self.config.getTag()
        if branch.startswith(tagPrefix):
            branch = Tag(branch)
        else:
            branch = Branch(branch)

        return branch

    def run(self, branch: [Branch, Tag]):
        remote = self.getRemote()
        controller= CompareController()
        currentBranch = controller.getCurrentBranch()
        repository = controller.getRepository()

        if type(branch) is Branch:
            self.checkBranch(remote, branch)
        elif type(branch) is Tag:
            self.checkTag(remote, branch)

        controller.compare(currentBranch, branch, remote)
