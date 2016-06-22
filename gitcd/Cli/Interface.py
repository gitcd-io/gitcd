import os
import re
import readline

class Interface(object):

  # style
  HEADER = '\033[95m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  
  # good
  OKBLUE = '\033[96m'
  OKGREEN = '\033[92m'
  
  # not so good
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  
  # closing character
  ENDC = '\033[0m'

  def writeOut(self, msg: str):
    print(msg)
    return True

  def error(self, msg: str):
    # some cli colors
    self.writeOut(self.FAIL + "Error: " + self.ENDC)
    return self.writeOut(msg)

  def warning(self, msg: str):
    # some cli colors
    return self.writeOut(self.WARNING + msg + self.ENDC)

  def header(self, msg: str):
    # some cli colors
    return self.writeOut(self.HEADER + msg + self.ENDC)

  def info(self, msg: str):
    # some cli colors
    return self.writeOut(self.OKBLUE + msg + self.ENDC)

  def ok(self, msg: str):
    # some cli colors
    return self.writeOut(self.OKGREEN + msg + self.ENDC)

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


class InputCompleter(object):

    options = []

    re = re.compile('.*\s+$', re.M)

    def setOptions(self, options: list):
      self.options = options
      return True

    def completeNothing(self, text, state):
      return False

    def completeOptions(self, text, state):
        # need to simplify this much more
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
