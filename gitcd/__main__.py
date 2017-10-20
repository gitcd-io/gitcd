# PYTHON_ARGCOMPLETE_OK

import sys
import argcomplete
import argparse
from gitcd.Gitcd import Gitcd
from gitcd.Cli.Interface import Interface

interface = Interface()

gitcd = Gitcd()
gitcd.setInterface(interface)
gitcd.setConfigFilename(".gitcd")
gitcd.setConfigFilenamePersonal(".gitcd-personal")
gitcd.loadConfig()

if len(sys.argv) == 2:
    # default branch name is *
    sys.argv.append('*')

# create parser in order to autocomplete
parser = argparse.ArgumentParser()

parser.add_argument(
    "command",
    help="Command to call.",
    type=str,
    choices=gitcd.getAvailableCommands()
)
parser.add_argument(
    "branch",
    help="Your awesome feature-branch name",
    type=str
)
argcomplete.autocomplete(parser)


def main():
    try:
        arguments = parser.parse_args()
        command = arguments.command
        branch = arguments.branch
        gitcd.dispatch(command, branch)
        sys.exit(0)
    except KeyboardInterrupt:
        interface.ok("So sad to say goodbye already...")
        sys.exit(1)
