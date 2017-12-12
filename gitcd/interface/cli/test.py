from gitcd.interface.cli.abstract import BaseCommand
from gitcd.controller.test import Test as TestController


class Test(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd test')

        controller = TestController()
        remote = self.getRemote()

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
            self.cli.execute("git checkout %s" % (featureBranch))

        except GitcdNoDevelopmentBranchDefinedException as e:
            self.interface.writeOut("gitcd error: %s" % (format(e)))

