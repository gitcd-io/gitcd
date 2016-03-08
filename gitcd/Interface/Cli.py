#!/usr/bin/env python3

import os
import re
import readline

from gitcd.Interface.AbstractInterface import AbstractInterface

"""
Cli interface class, currently just used to mojo-fy the output with some colors.
"""
class Cli(AbstractInterface):
  
  """
  Different colors for cli
  """
  # style
  HEADER = '\033[95m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  
  # good
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  
  # not so good
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  
  # closing character
  ENDC = '\033[0m'
  

  """
  error: Displays the error message on command line

    @arg msg:str    Message to display before exit
    @return bool    Returns True
  """
  def error(self, msg: str):
    # some cli colors
    self.writeOut(self.FAIL + "Error: " + self.ENDC)
    return self.writeOut(msg)

  """
  warning: Displays a message as header

    @arg msg:str    Message to display
    @return bool    Returns True
  """
  def warning(self, msg: str):
    # some cli colors
    self.writeOut(self.WARNING + "Warning: " + self.ENDC)
    return self.writeOut(msg)

  """
  header: Displays a message as header

    @arg msg:str    Message to display
    @return bool    Returns True
  """
  def header(self, msg: str):
    # some cli colors
    return self.writeOut(self.HEADER + msg + self.ENDC)

  """
  info: Displays a message as info

    @arg msg:str    Message to display
    @return bool    Returns True
  """
  def info(self, msg: str):
    # some cli colors
    return self.writeOut(self.OKBLUE + msg + self.ENDC)

  """
  ok: Displays a message as ok

    @arg msg:str    Message to display
    @return bool    Returns True
  """ 
  def ok(self, msg: str):
    # some cli colors
    return self.writeOut(self.OKGREEN + msg + self.ENDC)

  """
  askFor: Ask for user input, reask if invalid answer given.

    @arg msg:str        Question to ask
    @arg optoions:mixed List with possible options or string "os.directory" for os directory tab completion
    @arg default:str    Default string 
    @return bool        Returns True
  """ 
  def askFor(self, prompt: str, options = False, default: str = False):
    self.info(prompt)

    completer = InputCompleter()
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")

    # given options completer
    if type(options) == list:
      self.writeOut(self.BOLD + "Possibilities: " + self.ENDC + "[" + ", ".join(options) +  "]")
      completer.setOptions(options)
      readline.set_completer(completer.completeOptions)

    # directory completer
    if type(options) == str and options == "os.directory":
      # just here to clarify, do nothing is perfect for /folder/completion if readline is parsed and bound
      pass

    # if no options set, use an empty completer as default
    if options == False:
      readline.set_completer(completer.completeNothing)
    if default:
      self.writeOut(self.BOLD + "Default: " + self.ENDC + default)

    value = input("")

    # reset all completers after user input is happen
    readline.set_completer()

    if type(value) == str:
      value = value.strip()

    if value == "" and default != False:
      value = default

    if type(options) == list and value not in options:
      self.error("Value <" + value + "> not allowed! Choose one of " + ", ".join(options))
      return self.askFor(prompt, options, default)
    return value


"""
Cli tab completion class.
"""
class InputCompleter(object):

    """
    Options list to complete with.
    """
    options = []

    """
    Regex for split user input by space.
    """
    re = re.compile('.*\s+$', re.M)

    """
    setOptions: Set list to complete with.

      @arg optoions:list List with possible options
      @arg default:str    Default string
      @return bool        Returns True
    """
    def setOptions(self, options: list):
      self.options = options
      return True

    """
    completeNothing: Empty completer

      @return bool        Returns False
    """
    def completeNothing(self, text, state):
      return False

    """
    completeOptions: Complete options

      @return bool        Returns True or False for tab completion with an options list
    """
    def completeOptions(self, text, state):
        # need to simplify this much more,l sure there is a lot to much
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        # show all commands
        if not line:
            return [c + ' ' for c in self.options][state]

        # account for last argument ending in a space
        if self.re.match(buffer):
            line.append('')
        
        # resolve command to the implementation function
        cmd = line[0].strip()
        if cmd in self.options:
            args = line[1:]
            if args:
                return False
            return [cmd + ' '][state]
        results = [c + ' ' for c in self.options if c.startswith(cmd)] + [None]
        return results[state]

