from gitcd.Git.Command import Command


class Finish(Command):

    def execute(self, branch: str):
        self.interface.header("gitcd feature finish")

        origin = self.getOrigin()

        featureBranch = self.getFeatureBranch(branch)

        if not self.checkBranch(origin, featureBranch):
            return False

        self.cli.execute("git checkout %s" % (self.config.getMaster()))
        self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))
        self.cli.execute("git merge %s/%s" % (origin, featureBranch))
        self.cli.execute("git push %s %s" % (origin, self.config.getMaster()))

        deleteFeatureBranch = self.interface.askFor(
            "Delete your feature branch?", ["yes", "no"], "yes"
        )

        if deleteFeatureBranch == "yes":
            # delete feature branch remote and locally
            self.cli.execute("git push %s :%s" % (origin, featureBranch))
            self.cli.execute("git branch -D %s" % (featureBranch))
