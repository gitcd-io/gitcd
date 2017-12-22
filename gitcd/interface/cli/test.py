from gitcd.interface.cli.abstract import BaseCommand
from gitcd.controller.test import Test as TestController
from gitcd.git.branch import Branch

from pprint import pprint


class Test(BaseCommand):

    def run(self, branch: Branch):
        self.interface.header('git-cd test')

        controller = TestController()
        remote = self.getRemote()
        developmentBranches = controller.getDevelopmentBranches()
        if len(developmentBranches) == 1:
            developmentBranch = developmentBranches[0]
        else:
            branchNames = []
            for developmentBranch in developmentBranches:
                branchNames.append(developmentBranch.getName())

            default = branchNames[0]
            choice = branchNames

            developmentBranch = Branch(self.interface.askFor(
                "Which develop branch you want to use?",
                choice,
                default
            ))

        controller.mergeBranch(remote, developmentBranch, branch)

