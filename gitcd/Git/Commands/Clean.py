from gitcd.Git.Command import Command

class Clean(Command):

  def run(self):
    self.update()
    self.getOrigin()
    self.interface.execute("git remote prune %s" % origin)