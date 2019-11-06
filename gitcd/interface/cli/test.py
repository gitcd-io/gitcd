from gitcd.interface.cli.abstract import BaseCommand
from gitcd.git.branch import Branch
from gitcd.git.repository import Repository


class Test(BaseCommand):

    updateRemote = True

    def run(self, branch: Branch):
        repository = Repository()
        remote = self.getRemote()
        developmentBranches = repository.getDevelopmentBranches()
        if len(developmentBranches) == 1:
            developmentBranch = developmentBranches[0]
        else:
            branchNames = []
            for developmentBranch in developmentBranches:
                branchNames.append(developmentBranch.getName())

            branchNames.reverse()
            default = branchNames[0]
            choice = branchNames

            developmentBranch = Branch(self.interface.askFor(
                "Which develop branch you want to use?",
                choice,
                default
            ))

        self.mergeWithRetry(remote, developmentBranch, branch)
        repository.checkoutBranch(branch)
