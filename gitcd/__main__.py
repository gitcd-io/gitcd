# PYTHON_ARGCOMPLETE_OK

import sys
import argcomplete
import argparse
from gitcd.Gitcd import Gitcd


gitcd = Gitcd()
gitcd.setConfigFilename(".gitcd")
gitcd.setConfigFilenamePersonal(".gitcd-personal")
gitcd.loadConfig()

# feature command expect always an action
if len(sys.argv) == 2 and sys.argv[1] != 'feature':
    # default action is run
    sys.argv.append('run')
# branch optional in any command
if len(sys.argv) == 3:
    # default branch name is *
    sys.argv.append('*')


def completeAction(prefix, parsed_args, **kwargs):
    return (
        v for v in gitcd.getCommand(
            parsed_args.command).getSubcommands() if v.startswith(prefix))

# create parser in order to autocomplete
parser = argparse.ArgumentParser()

parser.add_argument(
    "command",
    help="Command to call.",
    type=str,
    choices=gitcd.getAvailableCommands()
)
parser.add_argument(
    "action",
    help="Action to execute.",
    type=str
).completer = completeAction
# todo forward completer to native git branch completion
parser.add_argument(
    "branch",
    help="Your awesome feature-branch name",
    type=str
)
argcomplete.autocomplete(parser)


def main():
    arguments = parser.parse_args()
    command = arguments.command
    action = arguments.action
    branch = arguments.branch
    gitcd.dispatch(command, action, branch)

    sys.exit(0)