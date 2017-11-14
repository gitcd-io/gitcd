import sys

import simpcli
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

from gitcd.exceptions import GitcdException
# from gitcd.Git.Commands.Clean import Clean
# from gitcd.Git.Commands.Start import Start
# from gitcd.Git.Commands.Test import Test
# from gitcd.Git.Commands.Review import Review
# from gitcd.Git.Commands.Finish import Finish
# from gitcd.Git.Commands.Release import Release
# from gitcd.Git.Commands.Status import Status
# from gitcd.Git.Commands.Compare import Compare
# from gitcd.Git.Commands.Upgrade import Upgrade
# from gitcd.Git.Abstract import Abstract

from pprint import pprint

class Cli():

    cli = simpcli.Interface()
    
    commands = {
        'init': Init(),
        'clean': Clean(),
        'start': Start(),
        'test': Test(),
        'review': Review(),
        'finish': Finish(),
        'release': Release(),
        'status': Status(),
        'compare': Compare(),
        'upgrade': Upgrade()
    }

    def getAvailableCommands(self):
        return self.commands.keys()


    def dispatch(self, command: str, branch: str):
        try:
            commandObject = self.commands[command]
        except Exception as e:
            errorMessage = 'Command %s does not exists,' + \
                ' see gitcd --help for more information.' + \
                ' Exception was: %s'

            self.cli.error(
                errorMessage % (
                    command,
                    e
                )
            )
            sys.exit(1)

        try:
            commandObject.run(branch)
        # catch cli execution errors here
        except GitcdException as e:
            self.cli.error(format(e))