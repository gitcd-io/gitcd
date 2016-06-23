from gitcd.Git.Command import Command

class Clean(Command):

  def run(self, dummy: str):
    self.update()
    origin = self.getOrigin()
    self.quietCli.execute("git remote prune %s" % origin)

    localBranches = self.getLocalBranches()
    remoteBranches = self.getRemoteBranches(origin)

    for branch in localBranches:
      if branch not in remoteBranches:
        if self.getCurrentBranch() == branch:
          self.quietCli.execute("git checkout %s" % self.config.getMaster())
        self.cli.execute("git branch -D %s" % branch)
