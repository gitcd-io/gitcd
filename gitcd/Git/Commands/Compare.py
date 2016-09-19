from gitcd.Git.Command import Command


class Compare(Command):

    def execute(self, dummy: str):
        self.update()
        origin = self.getOrigin()
        currentBranch = self.getCurrentBranch()
        latestTag = self.getLatestTag()
        self.cli.execute("git diff %s %s --color" % (latestTag, currentBranch))
