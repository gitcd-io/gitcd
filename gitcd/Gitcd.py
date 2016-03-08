#!/usr/bin/env python3

from gitcd.Exceptions import GitcdException
#from gitcd.ConfigFile import ConfigFile as Gitcdfile
from gitcd.Config.File import File as ConfigFile
from gitcd.Interface.AbstractInterface import AbstractInterface
from gitcd.Interface.Cli import Cli


"""
Gitcd implementation.
"""
class Gitcd(object):
  """
  interface: knack.Interface.AbstractInterface.AbstractInterface
  """
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
    
    print("initialize gitcd tool")
  
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
