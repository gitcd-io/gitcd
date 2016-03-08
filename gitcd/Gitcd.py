#!/usr/bin/env python3

from gitcd.Exceptions import GitcdException

"""
Gitcd implementation.
"""
class Gitcd(object):


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
