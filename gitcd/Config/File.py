import os
import yaml
from gitcd.Config.Parser import Parser
from gitcd.Config.Defaults import Defaults


class File:

    loaded = False
    filename = ".gitcd"
    parser = Parser()
    defaults = Defaults()
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

    def getMaster(self):
        return self.config['master']

    def setMaster(self, master: str):
        self.config['master'] = master

    def getFeature(self):
        return self.config['feature']

    def setFeature(self, feature: str):
        self.config['feature'] = feature

    def getTest(self):
        return self.config['test']

    def setTest(self, test: str):
        self.config['test'] = test

    def getTag(self):
        return self.config['tag']

    def setTag(self, tag: str):
        self.config['tag'] = tag

    def getVersionType(self):
        return self.config['versionType']

    def setVersionType(self, versionType: str):
        self.config['versionType'] = versionType

    def getVersionScheme(self):
        return self.config['versionScheme']

    def setVersionScheme(self, versionType: str):
        self.config['versionScheme'] = versionType
