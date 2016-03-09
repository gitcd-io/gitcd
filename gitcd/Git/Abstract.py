from gitcd.Cli.Command import Command as CliCommand
from gitcd.Cli.Interface import Interface as CliInterface
from gitcd.Config.File import File as ConfigFile

class Abstract(object):

  cli = CliCommand()
  interface = CliInterface()
  config = False

  def setConfig(self, config: ConfigFile):
    self.config = config

  def update(self):
    self.cli.execute("git remote update")
