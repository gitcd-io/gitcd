import sys
from gitcd.Config.File import File as ConfigFile
from gitcd.Cli.Interface import Interface
from gitcd.Git.Git import Git
from gitcd.Git.Command import Command

class Gitcd(object):

  interface = Interface()
  config = ConfigFile()
  git = Git()

  def __init__(self):
    self.git.setConfig(self.config)
    self.git.setupCommands()

  def setConfigFilename(self, configFilename):
    self.config.setFilename(configFilename)

  def loadConfig(self):
    self.config.load()

  def getCommand(self, command):
    try:
      commandObject = self.git.commands[command]
    except:
      commandObject = Command()

    return commandObject

  def dispatch(self, command, action, branch):
    try:
      commandObject = self.git.commands[command]
    except:
      self.interface.error("Subcommand %s does not exists, see gitcd --help for more information." % command)
      sys.exit(1)
    
    try:
      subcommandMethod = getattr(commandObject, action)  
    except:
      self.interface.error("Action %s does not exists on subcommand %s, see gitcd --help for more information." % (action, command))
      sys.exit(1)

    # not sure if its really necessary to update everytime here, its good but takes some time
    self.git.update()
    subcommandMethod(branch)
