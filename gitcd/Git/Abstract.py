from gitcd.Config.File import File as ConfigFile
from gitcd.Config.FilePersonal import FilePersonal as ConfigFilePersonal
from gitcd.Cli.Command import Command as CliCommand
from gitcd.Cli.Interface import Interface as CliInterface

class Abstract(object):

  cli = CliCommand()
  quietCli = CliCommand()
  interface = CliInterface()
  config = False
  configPersonal = False

  def __init__(self):
    self.cli.setRaiseException(True)
    self.cli.setVerbose(True)
    self.quietCli.setRaiseException(True)
    self.quietCli.setVerbose(False)

  def setConfig(self, config: ConfigFile):
    self.config = config

  def setConfigPersonal(self, configPersonal: ConfigFilePersonal):
    self.configPersonal = configPersonal

  def update(self):
    self.quietCli.execute("git remote update")
    self.quietCli.execute("git fetch -p")
