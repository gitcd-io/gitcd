from gitcd.interface.cli.abstract import BaseCommand
from gitcd.git.branch import Branch
from gitcd.controller.finish import Finish as FinishController

from gitcd.exceptions import GitcdNoFeatureBranchException


class Finish(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd finish')

        controller = FinishController()
        remote = self.getRemote()
        currentBranch = controller.getCurrentBranch()
        featureAsString = self.config.getString(self.config.getFeature())
        repository = controller.getRepository()
        if branch == '*':
            featureBranch = currentBranch
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


        if repository.hasUncommitedChanges():
            abort = self.interface.askFor(
                "You currently have uncomitted changes." +
                " Do you want me to abort and let you commit first?",
                ["yes", "no"],
                "yes"
            )

            if abort == "yes":
                return False

        # check remote existence
        if not remote.hasBranch(featureBranch):
            pushFeatureBranch = self.interface.askFor(
                "Your feature branch does not exists on origin." +
                " Do you want me to push it remote?", ["yes", "no"], "yes"
            )

            if pushFeatureBranch == "yes":
                remote.push(featureBranch)

        # check behind origin
        if remote.isBehind(featureBranch):

            pushFeatureBranch = self.interface.askFor(
                "Your feature branch is ahead the origin/branch." +
                " Do you want me to push the changes?",
                ["yes", "no"],
                "yes"
            )

            if pushFeatureBranch == "yes":
                remote.push(featureBranch)

        controller.mergeIntoMaster(featureBranch, remote)

        deleteFeatureBranch = self.interface.askFor(
            "Delete your feature branch?", ["yes", "no"], "yes"
        )

        if deleteFeatureBranch == "yes":
            # delete feature branch remote and locally
            remote.delete(featureBranch)
            featureBranch.delete()
