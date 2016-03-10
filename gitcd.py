#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import sys
import argcomplete
import argparse

from gitcd.Gitcd import Gitcd


gitcd = Gitcd()
gitcd.setConfigFilename(".gitcd")
gitcd.loadConfig()

# create parser in order to autocomplete
parser = argparse.ArgumentParser()
parser.add_argument("command", help="Command to call.", type=str, choices=('init', 'feature', 'fart'))
parser.add_argument("action", help="Action to execute.", type=str, choices=('start', 'test', 'review', 'finish'))
parser.add_argument("branch", help="Your awesome feature-branch name", type=str)
argcomplete.autocomplete(parser)


def main(command: str, action: str, branch: str):
  # todo: abort if no .gitcd file is present or just go on with the defaults?
  if command == "init":
    gitcd.init()
  else:
    gitcd.dispatch(command, action, branch)

  sys.exit(0)


if __name__ == '__main__':
  arguments = parser.parse_args()
  main(arguments.command, arguments.action, arguments.branch)
