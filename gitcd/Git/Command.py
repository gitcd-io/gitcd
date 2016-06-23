from gitcd.Config.File import File as ConfigFile
from gitcd.Git.Abstract import Abstract
from gitcd.Exceptions import GitcdNoDevelopmentBranchDefinedException

class Command(Abstract):

  # meant to be overwritten in concrete command implementations
  def getSubcommands(self):
    return ['run']

  # basic default maethod for any command
  def run(self):
    return False

  # some abstract main functions for any command
  def getCurrentBranch(self):
    return self.quietCli.execute("git rev-parse --abbrev-ref HEAD")

  def getFeatureBranch(self, branch: str):
    if branch == "*":
      # todo, maybe check for featureBranch prefix, or at least check if its not the master/develop branch and not any tag
      # ask for any remote feature branch if conditions dont match
      featureBranch = self.getCurrentBranch()
    else:
      featureBranch = "%s%s" % (self.config.getFeature(), branch)

    return featureBranch

  def readDevelopmentBranches(self):
    output = self.quietCli.execute("git branch -r")
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

    if len(branches) < 1:
      raise GitcdNoDevelopmentBranchDefinedException("No development branch found")
    elif len(branches) == 1:
      developmentBranch = branches[0]
    else:
      if len(branches) == 0:
        default = False
        choice = False
      else:
        default = branches[0]
        choice = branches

        developmentBranch = self.interface.askFor("Which develop branch you want to use?", choice, default)

    return developmentBranch

  def readOrigins(self):
    output = self.quietCli.execute("git remote -v")
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

    if len(origins) == 1:
      origin = origins[0]
    else:
      if len(origins) == 0:
        default = False
        choice = False
      else:
        default = origins[0]
        choice = origins

        origin = self.interface.askFor("Which origin you want to use?", choice, default)

    return origin


  def getLocalBranches(self):
    output = self.quietCli.execute("git branch -a")
    if output == False:
      return []

    lines = output.split("\n")

    localBranches = []
    for line in lines:
      line = line.strip()
      if not line.startswith("remotes/"):
        localBranches.append(line.replace("* ", ""))

    return localBranches

  def getRemoteBranches(self, origin: str):
    output = self.quietCli.execute("git branch -r")
    if output == False:
      return []

    lines = output.split("\n")

    remoteBranches = []
    for line in lines:
      line = line.strip()
      if line.startswith("%s/" % origin):
        if not line.startswith("%s/HEAD" % origin): 
          remoteBranches.append(line.replace("%s/" % origin, ""))

    return remoteBranches
