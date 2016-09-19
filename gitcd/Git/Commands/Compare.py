from gitcd.Git.Command import Command


class Compare(Command):

    def execute(self, branchToCompare: str):
        self.update()
        origin = self.getOrigin()

        currentBranch = self.getCurrentBranch()
        if not self.checkBranch(origin, currentBranch):
            return False

        if branchToCompare == "*":
            branchToCompare = self.getLatestTag()

        origin = self.getOrigin()

        self.cli.execute("git diff %s %s/%s --color" % (
            branchToCompare,
            origin,
            currentBranch
        ))
