import sys
from gitcd.Config.File import File as ConfigFile
from gitcd.Cli.Interface import Interface
from gitcd.Git.Git import Git

class Gitcd(object):

  interface = Interface()
  config = ConfigFile()
  git = Git()

  def __init__(self):
    self.git.setConfig(self.config)
    self.git.setupCommands()

  def setConfigFilename(self, configFilename: str):
    self.config.setFilename(configFilename)

  def loadConfig(self):
    self.config.load()

  def getCommand(self):
    return 

  def dispatch(self, command: str, action: str, branch: str):
    try:
      commandObject = self.git.commands[command]
    except:
      self.interface.error("Subcommand %s does not exists, see gitcd --help for more information." % command)
      sys.exit(1)
    
    try:
      subcommandMethod = getattr(commandObject, action)  
    except:
      self.interface.error("Action %s does not exists on subcommand %s, see knack --help for more information." % action)
      sys.exit(1)

    # not sure if its really necessary to update everytime here, its good but takes some time
    self.git.update()
    subcommandMethod(branch)
