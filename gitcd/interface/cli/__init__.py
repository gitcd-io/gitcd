import sys

import simpcli

from gitcd.interface.cli.abstract import BaseCommand
from gitcd.interface.cli.clean import Clean
from gitcd.interface.cli.compare import Compare
from gitcd.interface.cli.finish import Finish
from gitcd.interface.cli.init import Init
from gitcd.interface.cli.release import Release
from gitcd.interface.cli.review import Review
from gitcd.interface.cli.start import Start
from gitcd.interface.cli.status import Status
from gitcd.interface.cli.test import Test
from gitcd.interface.cli.upgrade import Upgrade
from gitcd.interface.cli.refresh import Refresh

from gitcd.config import MoveGitcdPersonalPerRepo

from gitcd.exceptions import GitcdException
from simpcli import CliException


class Cli():

    interface = simpcli.Interface()

    commands = [
        'init',
        'clean',
        'start',
        'test',
        'review',
        'finish',
        'release',
        'status',
        'compare',
        'upgrade',
        'refresh'
    ]

    def getAvailableCommands(self):
        return self.commands

    def instantiateCommand(self, command: str) -> BaseCommand:
        if command == 'init':
            return Init()
        if command == 'clean':
            return Clean()
        if command == 'start':
            return Start()
        if command == 'test':
            return Test()
        if command == 'review':
            return Review()
        if command == 'finish':
            return Finish()
        if command == 'release':
            return Release()
        if command == 'status':
            return Status()
        if command == 'compare':
            return Compare()
        if command == 'upgrade':
            return Upgrade()
        if command == 'refresh':
            return Refresh()
        # probably best to implement a default command
        # for command-not-found error

    def dispatch(self, command: str, branch: str):
        # this is kind of temporary and will get removed in a few
        # releases. It ensures your access token, now stored in all repos
        # will be moved into a .gitcd directory in your home directory
        MoveGitcdPersonalPerRepo()

        try:
            commandObject = self.instantiateCommand(command)
        except GitcdException as e:
            self.interface.error(
                e
            )
            sys.exit(1)
        except Exception as e:
            self.interface.error(
                e
            )
            sys.exit(1)

        self.interface.header('git-cd %s' % (command))

        try:
            if branch == '*':
                branch = commandObject.getDefaultBranch()
            else:
                branch = commandObject.getRequestedBranch(branch)

            commandObject.run(branch)
        # catch cli execution errors here
        except (GitcdException, CliException) as e:
            self.interface.error(format(e))

    def close(self, msg: str):
        self.interface.ok(msg)
