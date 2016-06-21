import os
import yaml
from gitcd.Config.Parser import Parser
from gitcd.Config.Defaults import Defaults


class File:

  loaded = False
  filename = ".gitcd"
  parser = Parser()
  defaults = Defaults()
  config = False

  def setFilename(self, configFilename):
  	self.filename = configFilename

  def load(self):
    if not os.path.isfile(self.filename):
      self.config = self.defaults.load()
    else:
      self.config = self.parser.load(self.filename)
  
  def write(self):
    self.parser.write(self.filename, self.config)

  def getMaster(self):
    return self.config['master']

  def setMaster(self, master):
    self.config['master'] = master

  def getFeature(self):
    return self.config['feature']

  def setFeature(self, feature):
    self.config['feature'] = feature

  def getTest(self):
    return self.config['test']

  def setTest(self, test):
    self.config['test'] = test

  def getTag(self):
    return self.config['tag']

  def setTag(self, tag):
    self.config['tag'] = tag

  def getVersionType(self):
    return self.config['versionType']

  def setVersionType(self, versionType: str):
    self.config['versionType'] = versionType

  def getVersionScheme(self):
    return self.config['versionScheme']

  def setVersionScheme(self, versionType: str):
    self.config['versionScheme'] = versionType

  def getToken(self):
    return self.config['token']

  def setToken(self, token):
    self.config['token'] = token
