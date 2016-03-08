#!/usr/bin/env python3


"""
Abstract interface class
"""
class AbstractInterface(object):


  """
  writeOut: Prints message

    @arg msg:str    Message to display before exit
    @return bool    Returns True
  """
  def writeOut(self, msg: str):
    print(msg)

    return True

  """
  error: Displays the error message on command line

    @arg msg:str    Message to display before exit
    @return bool    Returns True
  """ 
  def error(self, msg: str):
    return self.writeOut(msg)

  """
  warning: Displays a message as header

    @arg msg:str    Message to display
    @return bool    Returns True
  """ 
  def warning(self, msg: str):
    return self.writeOut(msg)

  """
  header: Displays a message as header

    @arg msg:str    Message to display
    @return bool    Returns True
  """ 
  def header(self, msg: str):
    return self.writeOut(msg)

  """
  info: Displays a message as info

    @arg msg:str    Message to display
    @return bool    Returns True
  """ 
  def info(self, msg: str):
    return self.writeOut(msg)

  """
  ok: Displays a message as ok

    @arg msg:str    Message to display
    @return bool    Returns True
  """ 
  def ok(self, msg: str):
    return self.writeOut(msg)

  """
  askFor: Ask for user input

    @arg msg:str        Question to ask
    @arg optoions:list  List with possible options
    @arg default:str    Default string 
    @return bool        Returns True
  """ 
  def askFor(self, prompt: str, options: list = False, default: str = False):
    raise Exception("Not implemented in abstract class gitcds.Interface.AbstractInterface.AbstractInterface")