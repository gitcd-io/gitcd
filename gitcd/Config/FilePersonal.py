import os
import yaml
from gitcd.Config.Parser import Parser
from gitcd.Config.DefaultsPersonal import DefaultsPersonal


class FilePersonal:

  loaded = False
  filename = ".gitcd-personal"
  parser = Parser()
  defaults = DefaultsPersonal()
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

  def getToken(self):
    return self.config['token']

  def setToken(self, token):
    self.config['token'] = token
