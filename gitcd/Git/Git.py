from gitcd.Git.Commands.Init import Init
from gitcd.Git.Commands.Clean import Clean
from gitcd.Git.Commands.Feature import Feature

class Git(object):

  commands = {
    'init': Init(),
    'clean': Clean(),
    'feature': Feature()
  }

  def setupCommands(self):
    self.commands['init'].setConfig(self.config)
    self.commands['clean'].setConfig(self.config)
    self.commands['feature'].setConfig(self.config)
