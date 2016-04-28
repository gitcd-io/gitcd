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

  def readOrigins(self):
    return ['origin', 'remote']

  def getOrigin(self):
    origins = self.readOrigins()
    if len(origins) > 1:
      origin = self.interface.askFor("Which origin you want to use?",
        origins,
        origins[0]
      )
    else:
      origin = origins[0]
    return origin

  def readRemotes(self):
    return ["https://github.com/claudio-walser/gitcd", "https://github.com/srf-mmz/gitcd"]

  def getRemote(self):
    remotes = self.readRemotes()
    if len(remotes) > 1:
      remote = self.interface.askFor("Which remote url you want to use?",
        remotes,
        remotes[0]
      )
    else:
      remote = remotes[0]
    return remote 