from gitcd.Git.Command import Command
from gitcd.Exceptions import GitcdNoDevelopmentBranchDefinedException


class Test(Command):

    def execute(self, branch: str):
        try:
            self.interface.header("gitcd feature test")

            origin = self.getOrigin()
            developmentBranch = self.getDevelopmentBranch()
            featureBranch = self.getFeatureBranch(branch)

            if not self.checkBranch(origin, featureBranch):
                return False

            self.cli.execute("git checkout %s" % (developmentBranch))
            self.cli.execute("git pull %s %s" % (origin, developmentBranch))
            self.cli.execute("git merge %s/%s" % (origin, featureBranch))
            self.cli.execute("git push %s %s" % (origin, developmentBranch))

        except GitcdNoDevelopmentBranchDefinedException as e:
            self.interface.writeOut("gitcd error: %s" % (format(e)))
