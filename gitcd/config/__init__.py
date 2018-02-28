import os
import yaml

from gitcd.config.defaults import GitcdDefaults
from gitcd.config.defaults import GitcdPersonalDefaults
from gitcd.exceptions import GitcdFileNotFoundException
from gitcd.exceptions import GitcdTokenNotImplemented


class Parser:

    yaml = {}

    def load(self, filename: str):
        # raise exception if no .gitcd in current working dir
        if not os.path.isfile(filename):
            raise GitcdFileNotFoundException("File %s not found" % filename)

        # open and load .gitcd
        with open(filename, 'r') as stream:
            self.yaml = yaml.safe_load(stream)

        return self.yaml

    def write(self, filename: str, config: dict):
        with open(filename, "w") as outfile:
            outfile.write(yaml.dump(config, default_flow_style=False))


class Gitcd:

    loaded = False
    filename = ".gitcd"
    parser = Parser()
    defaults = GitcdDefaults()
    config = {}

    def __init__(self):
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

    def getString(self, value):
        if not isinstance(value, str):
            return ''
        else:
            return value

    def setFilename(self, configFilename: str):
        self.filename = configFilename

    def write(self):
        self.parser.write(self.filename, self.config)

    def getMaster(self):
        return self.config['master']

    def setMaster(self, master: str):
        self.config['master'] = master

    def getFeature(self):
        return self.config['feature']

    def setFeature(self, feature: str):
        if feature == '<none>':
            feature = None

        self.config['feature'] = feature

    def getTest(self):
        return self.config['test']

    def setTest(self, test: str):
        if test == '<none>':
            test = None

        self.config['test'] = test

    def getTag(self):
        return self.config['tag']

    def setTag(self, tag: str):
        if tag == '<none>':
            tag = None

        self.config['tag'] = tag

    def getVersionType(self):
        return self.config['versionType']

    def setVersionType(self, versionType: str):
        self.config['versionType'] = versionType

    def getVersionScheme(self):
        return self.config['versionScheme']

    def setVersionScheme(self, versionType: str):
        self.config['versionScheme'] = versionType

    def setExtraReleaseCommand(self, releaseCommand: str):
        if releaseCommand == '<none>':
            releaseCommand = None
        self.config['extraReleaseCommand'] = releaseCommand

    def getExtraReleaseCommand(self):
        return self.config['extraReleaseCommand']


class GitcdPersonal:

    loaded = False
    filename = "~/.gitcd/access-tokens"
    parser = Parser()
    defaults = GitcdPersonalDefaults()
    config = {}
    allowedTokenSpaces = ['github', 'bitbucket']

    def __init__(self):
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

    def setFilename(self, configFilename: str):
        self.filename = configFilename

    def write(self):
        self.parser.write(self.filename, self.config)

    def getToken(self, tokenSpace: str):
        if tokenSpace not in self.allowedTokenSpaces:
            raise GitcdTokenNotImplemented(
                "Only tokens for '%s' are implemented!" % (
                    self.allowedTokenSpaces.join(', ')
                )
            )
        return self.config['tokens'][tokenSpace]

    def setToken(self, tokenSpace: str, token: str):
        if tokenSpace not in self.allowedTokenSpaces:
            raise GitcdTokenNotImplemented(
                "Only tokens for '%s' are implemented!" % (
                    self.allowedTokenSpaces.join(', ')
                )
            )
        self.config['tokens'][tokenSpace] = token


class MoveGitcdPersonalPerRepo:

    filename = '.gitcd-personal'
    parser = Parser()
    config = {}

    def __init__(self):
        if os.path.isfile(self.filename):
            self.config = self.parser.load(self.filename)
            self.move()

    def move(self):
        newConfigFile = GitcdPersonal()
        if 'token' in self.config and type(self.config['token']) is str:
            newConfigFile.setToken('github', self.config['token'])
            newConfigFile.write()
            os.remove(self.filename)

        # remove from .gitignore - not sure if this is smart
        # since the file could still be here for other users
        # and could therefore be commited by accident.
        # i may let this to the user
        gitignore = ".gitignore"
        if not os.path.isfile(gitignore):
            gitignoreContent = self.filename
        else:
            with open(gitignore, "r") as gitignoreFile:
                gitignoreContent = gitignoreFile.read()
            # if not yet in gitignore
            if "%s" % (self.filename) not in gitignoreContent:
                # add it
                gitignoreContent = gitignoreContent.replace(
                    "\n%s\n" % (self.filename),
                    ''
                )

        with open(gitignore, "w") as gitignoreFile:
            gitignoreFile.write(gitignoreContent)
