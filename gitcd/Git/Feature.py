from gitcd.Git.Abstract import Abstract
import time


#from gitcd.Exceptions import GitcdException
#from gitcd.Config.File import File as ConfigFile
#from gitcd.Interface.AbstractInterface import AbstractInterface
#from gitcd.Interface.Cli import Cli
#from gitcd.Git.Common import Common

class Feature(Abstract):

  # maybe even take this in a own feature class
  def start(self, branch: str):
    self.interface.ok("gitcd feature start")

    # todo: uh, need to fetch origin from .git somehow
    # possibly from `git remote -v`
    self.cli.execute("git checkout %s" % (self.config.getMaster()))
    self.cli.execute("git pull origin %s" % (self.config.getMaster()))
    self.cli.execute("git checkout -b %s%s" % (self.config.getFeature(), branch))
    self.cli.execute("git push origin %s%s" % (self.config.getFeature(), branch))

  def test(self, branch: str):
    self.interface.ok("gitcd feature test")

    # todo: need to handle this as prefix and read all possible branches
    # ask user if more than one possibillities
    self.cli.execute("git checkout %s" % (self.config.getTest()))
    self.cli.execute("git pull origin %s" % (self.config.getTest()))
    self.cli.execute("git merge %s%s" % (self.config.getFeature(), branch))
    self.cli.execute("git push origin %s" % (self.config.getTest()))

  def review(self, branch: str):
    self.interface.ok("open a pull request on github")
    # todo: need to fetch url from .git file or cli commands
    # possibly from `git remote -v`
    self.cli.execute("git request-pull %s%s https://github.com/mmz-srf/srf-mpc %s" % (self.config.getFeature(), branch, self.config.getMaster()))


  def finish(self, branch: str):
    self.interface.ok("gitcd feature finish")

    self.cli.execute("git checkout %s" % (self.config.getMaster()))
    self.cli.execute("git pull origin %s" % (self.config.getMaster()))
    self.cli.execute("git merge %s%s" % (self.config.getFeature(), branch))
    self.cli.execute("git push origin %s" % (self.config.getMaster()))

    # push new tag
    currentDate = time.strftime("%Y-%m-%d-%H%M")
    # need to handle commit message here, interactive shell execution could be a possiblity
    self.cli.execute("git tag -a -m 'release' %s%s" % (self.config.getTag(), currentDate))
    self.cli.execute("git push origin %s%s" % (self.config.getTag(), currentDate))

    deleteFeatureBranch = self.interface.askFor("Delete your feature branch?",
      ["yes", "no"],
      "yes"
    )

    if deleteFeatureBranch == "yes":
      # feature branch lokal und remote wieder löschen
      self.cli.execute("git branch -D %s%s" % (self.config.getFeature(), branch))
      self.cli.execute("git push origin :%s%s" % (self.config.getFeature(), branch))
