from gitcd.Cli.Command import Command as CliCommand
from gitcd.Cli.Interface import Interface as CliInterface
from gitcd.Config.File import File as ConfigFile

class Abstract(object):

  cli = CliCommand()
  interface = CliInterface()
  config = False

  def setConfig(self, config:ConfigFile):
    self.config = config

  def update(self):
    self.cli.execute("git remote update")

  def readDevelopmentBranches(self):
    output = self.cli.execute("git branch -r")

    if output == False:
      return []

    lines = output.split("\n")

    branches = []
    for line in lines:
      line = line.strip()
      if line.startswith("origin/%s" % self.config.getTest()):
        branches.append(line.replace("origin/", ""))

    return branches

  def getDevelopmentBranch(self):
    branches = self.readDevelopmentBranches()

    if len(branches) == 0:
      self.interface.error("An error occured while reading your development branches. Please pass it manually!")
      # should ask for user input here as well

    else if len(branches) > 1:
      currentDevelopmentBranch = self.interface.askFor("Which origin you want to use?",
        branches,
        branches[0]
      )
    else:
      currentDevelopmentBranch = branches[0]

    return currentDevelopmentBranch


  def readOrigins(self):
    output = self.cli.execute("git remote -v")
    if output == False:
      self.interface.error("An error occured while reading remotes. Please pass it manually!")
      return []

    lines = output.split("\n")

    last = False
    origins = []
    for line in lines:
        strings = line.split("\t")
        if last != strings[0] and strings[0] != "":
            last = strings[0]
            origins.append(last)

    return origins

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
    output = self.cli.execute("git remote -v")
    if output == False:
      self.interface.error("An error occured while reading remotes. Please pass it manually!")
      return []

    lines = output.split("\n")

    last = False
    remotes = []
    for line in lines:
        strings = line.split("\t")
        if last != strings[1] and strings[1] != "":
            last = strings[1]
            remotes.append(last)

    return remotes

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