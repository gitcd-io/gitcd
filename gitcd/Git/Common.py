from gitcd.Git.Abstract import Abstract
from gitcd.Git.Feature import Feature

class Common(Abstract):

  subCommands = {
    'feature': Feature()
  }

  def setupSubcommands(self):
    self.subCommands['feature'].setConfig(self.config)
