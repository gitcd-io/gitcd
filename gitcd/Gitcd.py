import sys
from gitcd.Config.File import File as ConfigFile
from gitcd.Config.FilePersonal import FilePersonal as ConfigFilePersonal
from gitcd.Cli.Interface import Interface
from gitcd.Git.Git import Git
from gitcd.Git.Command import Command
from gitcd.Exceptions import GitcdCliExecutionException


class Gitcd(object):

    interface = Interface()
    config = ConfigFile()
    configPersonal = ConfigFilePersonal()
    git = Git()

    def __init__(self):
        self.git.setConfig(self.config)
        self.git.setConfigPersonal(self.configPersonal)
        self.git.setupCommands()

    def setConfigFilename(self, configFilename: str):
        self.config.setFilename(configFilename)

    def setConfigFilenamePersonal(self, configFilenamePersonal: str):
        self.configPersonal.setFilename(configFilenamePersonal)

    def loadConfig(self):
        self.config.load()
        self.configPersonal.load()

    def getAvailableCommands(self):
        return self.git.commands.keys()

    def getCommand(self, command: str):
        try:
            commandObject = self.git.commands[command]
        except:
            commandObject = Command()

        return commandObject

    def dispatch(self, command: str, action: str, branch: str):
        try:
            commandObject = self.git.commands[command]
        except:
            self.interface.error(
                "Subcommand %s does not exists," +
                " see gitcd --help for more information." %
                command)
            sys.exit(1)

        try:
            subcommandMethod = getattr(commandObject, action)
        except:
            self.interface.error(
                "Action %s does not exists on subcommand %s," +
                " see gitcd --help for more information." %
                (action, command))
            sys.exit(1)

        try:
            # not sure if its really necessary to update everytime here, its
            # good but takes some time
            self.git.update()
            subcommandMethod(branch)
        # catch cli executino errors here
        except GitcdCliExecutionException as e:
            self.interface.error(format(e))
