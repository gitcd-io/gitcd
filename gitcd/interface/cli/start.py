from gitcd.interface.cli.abstract import BaseCommand
from gitcd.controller.start import Start as StartController
from pprint import pprint


class Start(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd start')

        remote = self.getRemote()
        masterBranch = self.config.getMaster()
        featurePrefix = self.config.getFeature()
        featurePrefixAsString = self.config.getString(featurePrefix)
        testBranch = self.config.getTest()
        testBranchAsString = self.config.getString(testBranch)

        # ask for branch if nothing passed
        if branch == "*":
            branch = self.interface.askFor(
                "Name for your new feature-branch? (without %s prefix)"
                % (featurePrefixAsString)
            )

        if '%s%s' % (featurePrefixAsString, branch) == masterBranch:
            # maybe i should use while here
            # if anyone passes master again, i wouldnt notice
            branch = self.interface.askFor(
                "You passed your master branch name as feature branch,\
                please give a different name."
            )

        # not sure if this is smart since test branch is kind of a prefix too
        if testBranch is not None:
            if '%s%s' % (featurePrefixAsString, branch).startswith(testBranchAsString):
                # maybe i should use while here
                # if anyone passes develop again, i wouldnt notice
                branch = self.interface.askFor(
                    "You passed your test branch name as feature branch,\
                    please give a different name."
                )

        if featurePrefix is not None:
            if branch.startswith(featurePrefixAsString):
                fixFeatureBranch = self.interface.askFor(
                    "Your feature branch already starts" +
                    " with your feature prefix," +
                    " should i remove it for you?",
                    ["yes", "no"],
                    "yes"
                )

                if fixFeatureBranch == "yes":
                    branch = branch.replace(featurePrefixAsString, "")

        featureBranch = "%s%s" % (
            featurePrefixAsString,
            branch
        )

        controller = StartController()
        controller.start(featureBranch, remote)
