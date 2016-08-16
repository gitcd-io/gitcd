from gitcd.Git.Command import Command


class Start(Command):

    def execute(self, branch: str):
        self.interface.header("gitcd start")

        origin = self.getOrigin()
        featurePrefix = self.config.getFeature()
        testBranch = self.config.getTest()
        masterBranch = self.config.getMaster()

        # ask for branch if nothing passed
        if branch == "*":
            branch = self.interface.askFor(
                "Name for your new feature-branch? (without %s prefix)"
                % self.config.getString(self.config.getFeature())
            )

        if testBranch is not None:
            if branch == testBranch:
                # maybe i should use recursion here
                # if anyone passes develop again, i wouldnt notice
                branch = self.interface.askFor(
                    "You passed your test branch name as feature branch,\
                    please give a different name."
                )

        if branch == masterBranch:
            # maybe i should use recursion here
            # if anyone passes master again, i wouldnt notice
            branch = self.interface.askFor(
                "You passed your master branch name as feature branch,\
                please give a different name."
            )

        if featurePrefix is not None:
            if branch.startswith(featurePrefix):
                fixFeatureBranch = self.interface.askFor(
                    "Your feature branch already starts" +
                    " with your feature prefix," +
                    " should i remove it for you?",
                    ["yes", "no"],
                    "yes"
                )

                if fixFeatureBranch == "yes":
                    branch = branch.replace(self.config.getFeature(), "")

        featureBranch = "%s%s" % (
            self.config.getString(self.config.getFeature()),
            branch
        )

        self.cli.execute(
            "git checkout %s" % (self.config.getMaster())
        )
        self.cli.execute(
            "git pull %s %s" % (origin, self.config.getMaster())
        )
        self.cli.execute(
            "git checkout -b %s" % (featureBranch)
        )
        self.cli.execute(
            "git push %s %s" % (origin, featureBranch)
        )
        self.cli.execute(
            "git branch --set-upstream-to %s/%s" % (origin, featureBranch)
        )
