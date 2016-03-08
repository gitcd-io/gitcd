from gitcd.Exceptions import GitcdException
from gitcd.Config.File import File as ConfigFile
from gitcd.Interface.AbstractInterface import AbstractInterface
from gitcd.Interface.Cli import Cli

from pprint import pprint

class Gitcd(object):


  interface = False
  configFile = ConfigFile()

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


  
  def feature(self):
    print("wrapper function, still needs a command as argument")

  def featureStart(self):
    print("gitcd feature start")

  def featureTest(self):
    print("gitcd feature test")

  def featureFinish(self):
    print("gitcd feature finish")

  def featureDeploy(self):
    print("gitcd feature deploy")
