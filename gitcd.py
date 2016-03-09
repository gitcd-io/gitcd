#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import sys
import argcomplete
import argparse

from gitcd.Gitcd import Gitcd
from gitcd.Interface.Cli import Cli

from pprint import pprint

"""
This is the main cli script for gitcd.
Mpcd is a tool for continous delivery for github projects

Link this in your local binary directory like this:
  sudo ln -s `pwd`/gitcd.py /usr/local/bin/gitcd

Its basicly a dispatcher using argparse.
"""

"""
gitcd instance
"""
interface = Cli()
gitcd = Gitcd()
gitcd.setInterface(interface)
gitcd.setConfigFilename(".gitcd")
gitcd.loadConfig()

if len(sys.argv) == 1:
  sys.argv.append('*')

if len(sys.argv) == 2:
  sys.argv.append('*')

def testCompleter(prefix, parsed_args, **kwargs):
  with open("./debug.txt", "w") as outfile:
    outfile.write(parsed_args)

  if  parsed_args[0] == "feature":
    possibleArgs = gitcd.getFeatureArgs()

  if parsed_args[0] == "init":
    possibleArgs = ["*"]

  return (v for v in possibleArgs if v.startswith(prefix))



# create parser in order to autocomplete
parser = argparse.ArgumentParser()
parser.add_argument("action", help="Action to call.", type=str, choices=('init', 'feature'))
# todo: make it optional as in https://github.com/claudio-walser/knack/blob/master/knack.py#L29
parser.add_argument("command", default="*", help="Command to execute.", type=str, choices=('start', 'test', 'review', 'finish', '*'))#.completer = testCompleter
# todo: make it optional as in https://github.com/claudio-walser/knack/blob/master/knack.py#L29
parser.add_argument("branch", default="*", help="Your awesome feature-branch name", type=str)
argcomplete.autocomplete(parser)


def main(action: str, command: str, branch: str):
  # todo: abort if no .gitcd file is present or just go on with the defaults?
  try:
    methodToCall = getattr(gitcd, action)  
  except:
    interface.error("Action %s does not exists, see gitcd --help for more information." % action)
    sys.exit(1)

  if action == "init":
    result = methodToCall()
  else:
    result = methodToCall(command, branch)

  sys.exit(0)


"""
Handle main loop
"""
if __name__ == '__main__':
  arguments = parser.parse_args()
  main(arguments.action, arguments.command, arguments.branch)
