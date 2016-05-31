#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import sys
import argcomplete
import argparse

from gitcd.Gitcd import Gitcd

from pprint import pprint

gitcd = Gitcd()
gitcd.setConfigFilename(".gitcd")
gitcd.loadConfig()

if len(sys.argv) == 2 and sys.argv[1] != 'feature':
  # default action is run
  sys.argv.append('run')
if len(sys.argv) == 3 and sys.argv[1] != 'feature':
  # default branch name is *
  sys.argv.append('*')

def completeAction(prefix, parsed_args, **kwargs):
  return (v for v in gitcd.getCommand(command).getSubcommands() if v.startswith(prefix))

# create parser in order to autocomplete
parser = argparse.ArgumentParser()
parser.add_argument("command", help="Command to call.", type=str, choices=('init', 'clean', 'feature'))
parser.add_argument("action", help="Action to execute.", type=str).completer = completeAction
parser.add_argument("branch", help="Your awesome feature-branch name", type=str) # todo forward completer to native git branch completion
argcomplete.autocomplete(parser)


def main(command: str, action: str, branch: str):
  # todo: abort if no .gitcd file is present or just go on with the defaults?
  gitcd.dispatch(command, action, branch)

  sys.exit(0)


if __name__ == '__main__':
  arguments = parser.parse_args()
  main(arguments.command, arguments.action, arguments.branch)
