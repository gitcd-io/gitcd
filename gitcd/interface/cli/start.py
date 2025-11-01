from gitcd.interface.cli.abstract import BaseCommand
from gitcd.git.branch import Branch


class Start(BaseCommand):

    def getDefaultBranch(self) -> Branch:
        featurePrefix = self.config.getFeature()
        featurePrefixAsString = self.config.getString(featurePrefix)
        branch = self.interface.askFor(
            "Name for your new feature-branch? (without %s prefix)"
            % (featurePrefixAsString)
        )

        return self.instantiateBranch(branch.replace(' ', '-'))

    def instantiateBranch(self, branch: str) -> Branch:
        featurePrefix = self.config.getFeature()
        featurePrefixAsString = self.config.getString(featurePrefix)

        return Branch('%s%s' % (featurePrefixAsString, branch))

    def checkDoubleFeaturePrefix(self, branch: Branch) -> Branch:
        featurePrefix = self.config.getFeature()
        featurePrefixAsString = self.config.getString(featurePrefix)

        if not featurePrefix:
            return branch

        if branch.getName().startswith('%s%s' % (
            featurePrefixAsString,
            featurePrefixAsString
        )):
            fixFeatureBranch = self.interface.askFor(
                "Your feature branch already starts" +
                " with your feature prefix," +
                " should i remove it for you?",
                ["yes", "no"],
                "yes"
            )

            if fixFeatureBranch == "yes":
                branch = self.instantiateBranch(
                    branch.getName().replace('%s%s' % (
                        featurePrefixAsString,
                        featurePrefixAsString
                    ), '')
                )

        return branch

    def run(self, branch: Branch):
        remote = self.getRemote()
        masterBranch = self.config.getMaster()
        featurePrefix = self.config.getFeature()
        featurePrefixAsString = self.config.getString(featurePrefix)
        testBranch = self.config.getTest()
        testBranchAsString = self.config.getString(testBranch)

        # Check for uncommitted changes and offer to stash
        stashed = False
        if self.repository.hasUncommitedChanges():
            stashChanges = self.interface.askFor(
                "You have uncommitted changes." +
                " Do you want me to stash them and re-apply after" +
                " creating the new branch?",
                ["yes", "no"],
                "yes"
            )

            if stashChanges == "yes":
                self.repository.stash()
                stashed = True
            else:
                abort = self.interface.askFor(
                    "Do you want me to abort and let you" +
                    " commit or discard your changes first?",
                    ["yes", "no"],
                    "yes"
                )

                if abort == "yes":
                    import sys
                    sys.exit(1)

        # few checks on the new feature branch
        if '%s%s' % (featurePrefixAsString, branch.getName()) == masterBranch:
            # maybe i should use while here
            # if anyone passes master again, i wouldnt notice
            branch = self.instantiateBranch(self.interface.askFor(
                "You passed your master branch name as feature branch,\
                please give a different name."
            ))

        # not sure if this is smart since test branch is kind of a prefix too
        if testBranch is not None:
            featureBranchString = '%s%s' % (
                featurePrefixAsString,
                branch.getName()
            )
            if featureBranchString.startswith(testBranchAsString):
                # maybe i should use while here
                # if anyone passes develop again, i wouldnt notice
                branch = self.instantiateBranch(self.interface.askFor(
                    "You passed your test branch name as feature branch,\
                    please give a different name."
                ))

        branch = self.checkDoubleFeaturePrefix(branch)

        remote.createFeature(branch)

        # Re-apply stashed changes if we stashed them earlier
        if stashed:
            self.repository.stashPop()
