#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import sys
import argcomplete
import argparse

from gitcd.Gitcd import Gitcd
from gitcd.Interface.Cli import Cli

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
gitcd = Gitcd(interface)


# create parser in order to autocomplete
parser = argparse.ArgumentParser()
parser.add_argument("action", help="Action to call.", type=str, choices=('init', 'feature'))
parser.add_argument("command", help="Command to execute.", type=str, choices=('start', 'test', 'finish', 'deploy'))
parser.add_argument("branch", help="Your awesome feature-branch name", type=str)
argcomplete.autocomplete(parser)


def main(action: str, command: str, branch: str):
  # abort if not initialize and still no config
  if not gitcd.gitcdfile.loaded and not action == "init":
    interface.error("No .gitcdfile exists. Call gitcd init first. Aborting now!")
    sys.exit(1)

  try:
    methodToCall = getattr(gitcd, action)  
  except:
    # todo: call exception
    interface.error("Action %s does not exists, see gitcd --help for more information." % action)
    sys.exit(1)

    result = methodToCall(box)
  sys.exit(0)


"""
Handle main loop
"""
if __name__ == '__main__':
  arguments = parser.parse_args()
  main(arguments.type, arguments.action, arguments.branch)
