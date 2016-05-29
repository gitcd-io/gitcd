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

  def setFilename(self, configFilename: str):
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

  def setMaster(self, master: str):
    self.config['master'] = master

  def getFeature(self):
    return self.config['feature']

  def setFeature(self, feature: str):
    self.config['feature'] = feature

  def getTest(self):
    return self.config['test']

  def setTest(self, test: str):
    self.config['test'] = test

  def getTag(self):
    return self.config['tag']

  def setTag(self, tag: str):
    self.config['tag'] = tag

  def getToken(self):
    return self.config['token']

  def setToken(self, token):
    self.config['token'] = token
