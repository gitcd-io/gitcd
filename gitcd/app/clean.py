from gitcd.git.repository import Repository
from gitcd.git.branch import Branch
from gitcd.git.tag import Tag
from gitcd.app import App


class Clean(App):

    def __init__(self):
        self.repository = Repository()
        pass

    def getBranchesToDelete(self) -> [Branch]:
        remotes = self.repository.getRemotes()
        branches = self.repository.getBranches()

        branchesToDelete = []

        for branch in branches:
            deleteBranch = True
            for remote in remotes:
                if remote.hasBranch(branch):
                    deleteBranch = False

            if deleteBranch:
                branchesToDelete.append(branch)

        return branchesToDelete

    def deleteBranches(self, branches: [Branch] = []) -> bool:
        currentBranch = self.repository.getCurrentBranch()
        masterBranch = Branch(self.config.getMaster())

        for branch in branches:
            if branch.getName() == currentBranch.getName():
                currentBranch = self.repository.checkoutBranch(masterBranch)
            branch.delete()

        return True
