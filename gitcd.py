#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import sys
import argcomplete
import argparse

from gitcd.Gitcd import Gitcd

from pprint import pprint

gitcd = Gitcd()
gitcd.setConfigFilename(".gitcd")
gitcd.loadConfig()

if len(sys.argv) == 2 and sys.argv[1] == 'init':
  sys.argv.append('*')
if len(sys.argv) == 3 and sys.argv[1] == 'init':
  sys.argv.append('*')

def completeAction(prefix, parsed_args, **kwargs):
  if parsed_args.command == 'feature':
    return (v for v in gitcd.getFeatureSubcommands() if v.startswith(prefix))

# create parser in order to autocomplete
parser = argparse.ArgumentParser()
parser.add_argument("command", help="Command to call.", type=str, choices=('init', 'feature'))
parser.add_argument("action", help="Action to execute.", type=str).completer = completeAction
parser.add_argument("--branch", "-b", help="Your awesome feature-branch name", type=str)
argcomplete.autocomplete(parser)


def main(command, action, branch):
  # todo: abort if no .gitcd file is present or just go on with the defaults?
  if command == "init":
    gitcd.init()
  else:
    gitcd.dispatch(command, action, branch)

  sys.exit(0)


if __name__ == '__main__':
  arguments = parser.parse_args()
  main(arguments.command, arguments.action, arguments.branch)
