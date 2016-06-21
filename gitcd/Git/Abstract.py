from gitcd.Config.File import File as ConfigFile
from gitcd.Cli.Command import Command as CliCommand
from gitcd.Cli.Interface import Interface as CliInterface

class Abstract(object):

  cli = CliCommand()
  interface = CliInterface()
  config = False

  def __init__(self):
    self.cli.setRaiseException(True)
    self.cli.setVerbose(True)

  def setConfig(self, config: ConfigFile):
    self.config = config

  def update(self):
    # dont be verbose on update
    verbose = self.cli.getVerbose()
    self.cli.setVerbose(False)
    self.cli.execute("git remote update")
    self.cli.execute("git fetch -p")
    self.cli.setVerbose(verbose)
