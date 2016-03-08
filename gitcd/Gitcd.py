#!/usr/bin/env python3

from gitcd.Exceptions import GitcdException
#from gitcd.ConfigFile import ConfigFile as Gitcdfile
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

  def __init__(self, interface: AbstractInterface):
    self.interface = interface

  def init(self):
    print("initialize gitcd tool")
  
  def status(self):
    print("gitcd status")

  def featureStart(self):
    print("gitcd feature start")

  def featureTest(self):
    print("gitcd feature test")

  def featureFinish(self):
    print("gitcd feature finish")

  def featureDeploy(self):
    print("gitcd feature deploy")
