from gitcd.Git.Commands.Init import Init
from gitcd.Git.Commands.Clean import Clean
from gitcd.Git.Commands.Feature import Feature
from gitcd.Git.Commands.Release import Release
from gitcd.Git.Abstract import Abstract


class Git(Abstract):

    commands = {
        'init': Init(),
        'clean': Clean(),
        'feature': Feature(),
        'release': Release()
    }

    def setupCommands(self):
        self.commands['init'].setConfig(self.config)
        self.commands['init'].setConfigPersonal(self.configPersonal)
        self.commands['clean'].setConfig(self.config)
        self.commands['clean'].setConfigPersonal(self.configPersonal)
        self.commands['feature'].setConfig(self.config)
        self.commands['feature'].setConfigPersonal(self.configPersonal)
        self.commands['release'].setConfig(self.config)
        self.commands['release'].setConfigPersonal(self.configPersonal)
