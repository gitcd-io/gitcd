import time
from gitcd.Exceptions import GitcdException
from gitcd.Config.File import File as ConfigFile
from gitcd.Interface.AbstractInterface import AbstractInterface
from gitcd.Interface.Cli import Cli
from gitcd.Cli.Command import Command as CliCommand

from pprint import pprint

class Gitcd(object):

  interface = False
  configFile = ConfigFile()
  cliCommand = CliCommand()

  featureMethods = {
    'start': 'featureStart',
    'test': 'featureTest',
    'review': 'featureReview',
    'finish': 'featureFinish'
  }

  def setInterface(self, interface: AbstractInterface):
    self.interface = interface

  def setConfigFilename(self, configFilename: str):
    self.configFile.setConfigFilename(configFilename)

  def loadConfig(self):
    # todo: maybe a warning if we are working with the default values
    self.configFile.load()

  def init(self):
    self.configFile.setMaster(
      self.interface.askFor("Branch name for production releases?",
      False,
      self.configFile.getMaster())
    )

    self.configFile.setFeature(
      self.interface.askFor("Branch name for feature development?",
      False,
      self.configFile.getFeature())
    )

    self.configFile.setTest(
      self.interface.askFor("Branch name for test releases?",
      False,
      self.configFile.getTest())
    )

    self.configFile.setTag(
      self.interface.askFor("Version tag prefix?",
      False,
      self.configFile.getTag())
    )

    self.configFile.write()
    pprint(self.configFile.config)

  def feature(self, command, branch):
    # remote upate
    self.update()

    # dispatch from mapping
    featureMethod = getattr(self, self.featureMethods[command])
    featureMethod(branch)

  def update(self):
    self.cliCommand.execute("git remote update")




  # maybe even take this in a own feature class
  def featureStart(self, branch: str):
    self.interface.ok("gitcd feature start")

    # todo: uh, need to fetch origin from .git somehow
    # possibly from `git remote -v`
    self.cliCommand.execute("git checkout %s" % (self.configFile.getMaster()))
    self.cliCommand.execute("git pull origin %s" % (self.configFile.getMaster()))
    self.cliCommand.execute("git checkout -b %s%s" % (self.configFile.getFeature(), branch))
    self.cliCommand.execute("git push origin %s%s" % (self.configFile.getFeature(), branch))

  def featureTest(self, branch: str):
    self.interface.ok("gitcd feature test")

    # todo: need to handle this as prefix and read all possible branches
    # ask user if more than one possibillities
    self.cliCommand.execute("git checkout %s" % (self.configFile.getTest()))
    self.cliCommand.execute("git pull origin %s" % (self.configFile.getTest()))
    self.cliCommand.execute("git merge origin %s%s" % (self.configFile.getFeature(), branch))
    self.cliCommand.execute("git push origin %s" % (self.configFile.getTest()))

  def featureReview(self, branch: str):
    self.interface.ok("open a pull request on github")
    # todo: need to fetch url from .git file or cli commands
    # possibly from `git remote -v`
    self.cliCommand.execute("git request-pull %s%s https://github.com/mmz-srf/srf-mpc %s" % (self.configFile.getFeature(), branch, self.configFile.getMaster()))


  def featureFinish(self, branch: str):
    self.interface.ok("gitcd feature finish")

    self.cliCommand.execute("git checkout %s" % (self.configFile.getMaster()))
    self.cliCommand.execute("git pull origin %s" % (self.configFile.getMaster()))
    self.cliCommand.execute("git merge origin %s%s" % (self.configFile.getFeature(), branch))
    self.cliCommand.execute("git push origin %s" % (self.configFile.getMaster()))

    # push new tag
    currentDate = time.strftime("%Y-%m-%d-%H%M")
    # need to handle commit message here, interactive shell execution could be a possiblity
    self.cliCommand.execute("git tag -a -m 'release' %s%s" % (self.configFile.getTag(), currentDate))
    self.cliCommand.execute("git push origin %s%s" % (self.configFile.getTag(), currentDate))

    deleteFeatureBranch = self.interface.askFor("Delete your feature branch?",
      ["yes", "no"],
      "yes"
    )
    if deleteFeatureBranch == "yes":
      # feature branch lokal und remote wieder löschen
      self.cliCommand.execute("git branch -D %s%s" % (self.configFile.getFeature(), branch))
      self.cliCommand.execute("git push origin :%s%s" % (self.configFile.getFeature(), branch))
