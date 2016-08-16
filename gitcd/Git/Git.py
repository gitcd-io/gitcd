from gitcd.Git.Commands.Init import Init
from gitcd.Git.Commands.Clean import Clean
from gitcd.Git.Commands.Start import Start
from gitcd.Git.Commands.Test import Test
from gitcd.Git.Commands.Review import Review
from gitcd.Git.Commands.Finish import Finish
from gitcd.Git.Commands.Release import Release
from gitcd.Git.Abstract import Abstract


class Git(Abstract):

    commands = {
        'init': Init(),
        'clean': Clean(),
        'start': Start(),
        'test': Test(),
        'review': Review(),
        'finish': Finish(),
        'release': Release()
    }

    def setupCommands(self):
        for command in self.commands:
            command.setConfig(self.config)
            command.setConfigPersonal(self.configPersonal)
