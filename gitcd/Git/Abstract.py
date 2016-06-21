from gitcd.Config.File import File as ConfigFile
from gitcd.Cli.Command import Command as CliCommand
from gitcd.Cli.Interface import Interface as CliInterface

class Abstract(object):

  cli = CliCommand()
  interface = CliInterface()
  config = False

  def __init__(self):
    self.cli.setRaiseException(True)

  def setConfig(self, config):
    self.config = config

  def update(self):
    self.cli.execute("git remote update")
    self.cli.execute("git fetch -p")