from gitcd.Git.Command import Command
import time

class Feature(Command):

  def getSubcommands(self):
    return [
      'start',
      'test',
      'review',
      'finish'
    ]

  def start(self, branch: str):
    self.interface.ok("gitcd feature start")

    origin = self.getOrigin()

    # ask for branch if nothing passed
    if branch == "*":
      branch = self.interface.askFor("Name for your new featur-branch?")

    branch = "%s%s" % (self.config.getFeature(), branch)


    self.cli.execute("git checkout %s" % (self.config.getMaster()))
    self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))
    self.cli.execute("git checkout -b %s" % (branch))
    self.cli.execute("git push %s %s%s" % (origin, self.config.getFeature(), branch))

  def test(self, branch: str):
    self.interface.ok("gitcd feature test")

    origin = self.getOrigin()
    developmentBranch = self.getDevelopmentBranch()

    if branch == "*":
      # todo, maybe check for featureBranch prefix, or at least check if its not the master/develop branch and not any tag
      branch = self.cli.execute("git rev-parse --abbrev-ref HEAD")
    else: 
      branch = "%s%s" % (self.config.getFeature(), branch)
      

    # todo: need to handle this as prefix and read all possible branches
    # ask user if more than one possibillities
    self.cli.execute("git checkout %s" % (developmentBranch))
    self.cli.execute("git pull %s %s" % (origin, developmentBranch))
    self.cli.execute("git merge %s" % (branch))
    self.cli.execute("git push %s %s" % (origin, developmentBranch))

  def review(self, branch: str):
    self.interface.ok("open a pull request on github")
    remote = self.getRemote()

    self.cli.execute("git request-pull %s%s %s %s" % (self.config.getFeature(), branch, remote, self.config.getMaster()))


  def finish(self, branch: str):
    self.interface.ok("gitcd feature finish")

    origin = self.getOrigin()

    self.cli.execute("git checkout %s" % (self.config.getMaster()))
    self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))
    self.cli.execute("git merge %s%s" % (self.config.getFeature(), branch))
    self.cli.execute("git push %s %s" % (origin, self.config.getMaster()))

    # push new tag
    currentDate = time.strftime("%Y.%m.%d%H%M")
    # need to handle commit message here, interactive shell execution could be a possiblity
    self.cli.execute("git tag -a -m 'release' %s%s" % (self.config.getTag(), currentDate))
    self.cli.execute("git push %s %s%s" % (origin, self.config.getTag(), currentDate))

    deleteFeatureBranch = self.interface.askFor("Delete your feature branch?",
      ["yes", "no"],
      "yes"
    )

    if deleteFeatureBranch == "yes":
      # delete feature branch locally and remote
      self.cli.execute("git branch -D %s%s" % (self.config.getFeature(), branch))
      self.cli.execute("git push %s :%s%s" % (origin, self.config.getFeature(), branch))
