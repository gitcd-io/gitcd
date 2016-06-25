from gitcd.Git.Commands.Init import Init
from gitcd.Git.Commands.Clean import Clean
from gitcd.Git.Commands.Feature import Feature
from gitcd.Git.Commands.Release import Release
from gitcd.Git.Abstract import Abstract

class Git(Abstract):

  commands = {
    'init': Init(),
    'clean': Clean(),
    'feature': Feature(),
    'release': Release()
  }

  def setupCommands(self):
    self.commands['init'].setConfig(self.config)
    self.commands['clean'].setConfig(self.config)
    self.commands['feature'].setConfig(self.config)
    self.commands['release'].setConfig(self.config)
