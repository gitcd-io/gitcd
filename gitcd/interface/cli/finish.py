from gitcd.interface.cli.abstract import BaseCommand
from gitcd.git.branch import Branch
from gitcd.controller.finish import Finish as FinishController

from gitcd.exceptions import GitcdNoFeatureBranchException


class Finish(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd finish')

        controller = FinishController()
        remote = self.getRemote()
        featureAsString = self.config.getString(self.config.getFeature())
        if branch == '*':
            featureBranch = controller.getCurrentBranch()
        else:
            featureBranch = Branch('%s%s' % (
                featureAsString,
                branch
            ))

        testBranch = self.config.getTest()
        masterBranch = self.config.getMaster()

        if featureBranch.getName() == masterBranch:
            # maybe i should use recursion here
            # if anyone passes master again, i wouldnt notice
            featureBranch = Branch('%s%s' % (
                featureAsString,
                self.interface.askFor(
                    "You passed your master branch name as feature branch,\
                    please give a different name."
                )
            ))

        if testBranch:
            if featureBranch.getName().startswith(testBranch):
                # maybe i should use recursion here
                # if anyone passes master again, i wouldnt notice
                featureBranch = Branch('%s%s' % (
                    featureAsString,
                    self.interface.askFor(
                        "You passed your test branch name as feature branch,\
                        please give a different name."
                    )
                ))

        # if still not a proper feature branch, raise an exception
        if not featureBranch.isFeature():
            raise GitcdNoFeatureBranchException(
                "Your current branch is not a valid feature branch." +
                " Checkout a feature branch or pass one as param."
            )

        print('your choosen feature branch is:')
        print(featureBranch.getName())
        pass


        # featureBranch = self.getFeatureBranch(branch)

        # if not self.checkBranch(origin, featureBranch):
        #     return False

        # self.cli.execute("git checkout %s" % (self.config.getMaster()))
        # self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))
        # self.cli.execute("git merge %s/%s" % (origin, featureBranch))
        # self.cli.execute("git push %s %s" % (origin, self.config.getMaster()))

        # deleteFeatureBranch = self.interface.askFor(
        #     "Delete your feature branch?", ["yes", "no"], "yes"
        # )

        # if deleteFeatureBranch == "yes":
        #     # delete feature branch remote and locally
        #     self.cli.execute("git push %s :%s" % (origin, featureBranch))
        #     self.cli.execute("git branch -D %s" % (featureBranch))

