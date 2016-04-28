import sys
from gitcd.Config.File import File as ConfigFile
from gitcd.Cli.Interface import Interface
from gitcd.Git.Common import Common as Git

class Gitcd(object):

  interface = Interface()
  config = ConfigFile()
  git = Git()

  def __init__(self):
    self.git.setConfig(self.config)
    self.git.setupSubcommands()

  def getFeatureSubcommands(self):
    return ['start', 'test', 'review', 'finish']

  def setConfigFilename(self, configFilename: str):
    self.config.setFilename(configFilename)

  def loadConfig(self):
    self.config.load()

  def init(self):
    self.config.setMaster(
      self.interface.askFor("Branch name for production releases?",
      False,
      self.config.getMaster())
    )

    self.config.setFeature(
      self.interface.askFor("Branch name for feature development?",
      False,
      self.config.getFeature())
    )

    self.config.setTest(
      self.interface.askFor("Branch name for test releases?",
      False,
      self.config.getTest())
    )

    self.config.setTag(
      self.interface.askFor("Version tag prefix?",
      False,
      self.config.getTag())
    )

    self.config.write()

  def dispatch(self, command: str, action: str, branch: str):
    try:
      subCommand = self.git.subCommands[command]  
    except:
      self.interface.error("Subcommand %s does not exists, see gitcd --help for more information." % command)
      sys.exit(1)
    
    try:
      method = getattr(subCommand, action)  
    except:
      self.interface.error("Action %s does not exists on subcommand %s, see knack --help for more information." % action)
      sys.exit(1)

    self.git.update()
    method(branch)
