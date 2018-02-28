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
        'upgrade'
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

    def dispatch(self, command: str, branch: str):
        moveLegacyConfig = MoveGitcdPersonalPerRepo()

        try:
            commandObject = self.instantiateCommand(command)
        except Exception as e:
            errorMessage = 'Command %s does not exists,' + \
                ' see gitcd --help for more information.' + \
                ' Exception was: %s'

            self.interface.error(
                errorMessage % (
                    command,
                    e
                )
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
