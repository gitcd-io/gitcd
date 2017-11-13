# PYTHON_ARGCOMPLETE_OK

import sys
import argcomplete
import argparse

from gitcd.interface.cli import Cli

if len(sys.argv) == 2:
    # default branch name is *
    sys.argv.append('*')

cli = Cli()

# create parser in order to autocomplete
parser = argparse.ArgumentParser()

parser.add_argument(
    "command",
    help="Command to call.",
    type=str,
    choices=cli.getAvailableCommands()
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
        cli.dispatch(command, branch)
        sys.exit(0)
    except KeyboardInterrupt:
        cli.ok("See you soon!")
        sys.exit(1)
