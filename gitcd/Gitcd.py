import sys
from gitcd.Config.File import File as ConfigFile
from gitcd.Config.FilePersonal import FilePersonal as ConfigFilePersonal
from gitcd.Git.Git import Git
from gitcd.Git.Command import Command
from gitcd.Exceptions import GitcdException


class Gitcd(object):

    config = ConfigFile()
    configPersonal = ConfigFilePersonal()
    git = Git()

    def __init__(self):
        self.git.setConfig(self.config)
        self.git.setConfigPersonal(self.configPersonal)
        self.git.setupCommands()

    def setInterface(self, interface):
        self.interface = interface

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
        except Exception:
            commandObject = Command()
        commandObject.setGit(self.git)
        return commandObject

    def dispatch(self, command: str, branch: str):
        try:
            commandObject = self.getCommand(command)
        except Exception:
            self.interface.error(
                "Command %s does not exists," +
                " see gitcd --help for more information." %
                command)
            sys.exit(1)

        try:
            # not sure if its really necessary to update everytime here, its
            # good but takes some time
            if command != 'upgrade':
                commandObject.update()

            commandObject.execute(branch)
        # catch cli execution errors here
        except GitcdException as e:
            self.interface.error(format(e))
