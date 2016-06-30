import os
import yaml
from gitcd.Config.Parser import Parser
from gitcd.Config.DefaultsPersonal import DefaultsPersonal


class FilePersonal:

    loaded = False
    filename = ".gitcd-personal"
    parser = Parser()
    defaults = DefaultsPersonal()
    config = {}

    def setFilename(self, configFilename: str):
        self.filename = configFilename

    def load(self):
        defaultConfig = self.defaults.load()
        if not os.path.isfile(self.filename):
            self.config = defaultConfig
        else:
            config = self.parser.load(self.filename)
            for key in defaultConfig.keys():
                if key in config:
                    self.config[key] = config[key]
                else:
                    self.config[key] = defaultConfig[key]

    def write(self):
        self.parser.write(self.filename, self.config)

        # add .gitcd-personal to .gitignore
        gitignore = ".gitignore"
        if not os.path.isfile(gitignore):
            gitignoreContent = self.filename
        else:
            with open(gitignore, "r") as gitignoreFile:
                gitignoreContent = gitignoreFile.read()
            # if not yet in gitignore
            if "\n%s\n" % (self.filename) not in gitignoreContent:
                # add it
                gitignoreContent = "%s\n%s\n" % (
                    gitignoreContent, self.filename)

        with open(gitignore, "w") as gitignoreFile:
            gitignoreFile.write(gitignoreContent)

    def getToken(self):
        return self.config['token']

    def setToken(self, token):
        self.config['token'] = token
