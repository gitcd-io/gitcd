from sys import platform

from gitcd.Config.File import File as ConfigFile
from gitcd.Git.Abstract import Abstract
from gitcd.Exceptions import GitcdNoDevelopmentBranchDefinedException
from gitcd.Exceptions import GitcdNoFeatureBranchException
from gitcd.Exceptions import GitcdNoRepositoryException


class Command(Abstract):

    # meant to be overwritten in concrete command implementations
    def getSubcommands(self):
        return ['run']

    # basic default maethod for any command
    def run(self):
        return False

    # some abstract main functions for any command
    def getCurrentBranch(self):
        return self.quietCli.execute("git rev-parse --abbrev-ref HEAD")

    def getFeatureBranch(self, branch: str):
        if branch == "*":
            featureBranch = self.getCurrentBranch()
            if not featureBranch.startswith(self.config.getFeature()):
                raise GitcdNoFeatureBranchException(
                    "Your current branch is not a valid feature branch.\
                    Checkout a feature branch or pass one as param.")
        else:
            featureBranch = "%s%s" % (self.config.getFeature(), branch)

        return featureBranch

    def readDevelopmentBranches(self):
        output = self.quietCli.execute("git branch -r")
        if not output:
            return []

        lines = output.split("\n")

        branches = []
        for line in lines:
            line = line.strip()
            if line.startswith("origin/%s" % self.config.getTest()):
                branches.append(line.replace("origin/", ""))

        return branches

    def getDevelopmentBranch(self):
        branches = self.readDevelopmentBranches()

        if len(branches) < 1:
            raise GitcdNoDevelopmentBranchDefinedException(
                "No development branch found")
        elif len(branches) == 1:
            developmentBranch = branches[0]
        else:
            if len(branches) == 0:
                default = False
                choice = False
            else:
                default = branches[0]
                choice = branches

                developmentBranch = self.interface.askFor(
                    "Which develop branch you want to use?", choice, default)

        return developmentBranch

    def readOrigins(self):
        output = self.quietCli.execute("git remote")
        if not output:
            self.interface.error(
                "An error occured while reading remotes.\
                Please pass it manually!")
            return []

        lines = output.split("\n")

        origins = []
        for line in lines:
            if line not in origins:
                origins.append(line)

        return origins

    def getOrigin(self):
        origins = self.readOrigins()

        if len(origins) == 1:
            origin = origins[0]
        else:
            if len(origins) == 0:
                default = False
                choice = False
            else:
                default = origins[0]
                choice = origins

            origin = self.interface.askFor(
                "Which origin you want to use?", choice, default)

        return origin

    def getLocalBranches(self):
        output = self.quietCli.execute("git branch -a")
        if not output:
            return []

        lines = output.split("\n")

        localBranches = []
        for line in lines:
            line = line.strip()
            if not line.startswith("remotes/"):
                localBranches.append(line.replace("* ", ""))

        return localBranches

    def getRemoteBranches(self, origin: str):
        output = self.quietCli.execute("git branch -r")
        if not output:
            return []

        lines = output.split("\n")

        remoteBranches = []
        for line in lines:
            line = line.strip()
            if line.startswith("%s/" % origin):
                if not line.startswith("%s/HEAD" % origin):
                    remoteBranches.append(line.replace("%s/" % origin, ""))

        return remoteBranches

    def getLocalTags(self):
        output = self.quietCli.execute("git tag -l")
        if not output:
            return []

        lines = output.split("\n")
        localTags = []
        for line in lines:
            localTags.append(line)

        return localTags

    def getRemoteTags(self, origin: str):
        output = self.quietCli.execute("git ls-remote --tags")
        if not output:
            return []

        lines = output.split("\n")

        remoteTags = []
        for line in lines:
            line = line.strip()
            if not line.startswith("From "):
                lineParts = line.split("\t")
                if len(lineParts) == 2:
                    tagName = lineParts[1]
                    if not tagName.endswith("^{}"):
                        remoteTags.append(tagName.replace("refs/tags/", ""))

        return remoteTags

    def getRemoteUrl(self, origin: str):
        output = self.quietCli.execute("git config -l")
        if not output:
            raise GitcdNoRepositoryException(
                "It seems you are not in any git repository")

        lines = output.split("\n")

        for line in lines:
            if line.startswith("remote.%s.url=" % (origin)):
                lineParts = line.split("=")
                url = lineParts[1]
                # in case of https
                # https://github.com/claudio-walser/test-repo.git
                if url.startswith("https://") or url.startswith("http://"):
                    url = url.replace("http://", "")
                    url = url.replace("https://", "")
                # in case of ssh git@github.com:claudio-walser/test-repo.git
                else:
                    urlParts = line.split("@")
                    url = urlParts[1]
                    url = url.replace(":", "/")

                return url

        raise GitcdNoRepositoryException(
            "It seems you are not in any git repository")

    def getUsername(self, origin: str):
        url = self.getRemoteUrl(origin)

        urlParts = url.split("/")
        username = urlParts[1]

        return username

    def getRepository(self, origin: str):
        url = self.getRemoteUrl(origin)

        urlParts = url.split("/")
        repository = urlParts[2]
        if repository.endswith(".git"):
            repository = repository.replace(".git", "")

        return repository

    def getDefaultBrowserCommand(self):
        if platform == "linux" or platform == "linux2":
            return "sensible-browser"
        elif platform == "darwin":
            return "open"
        elif platform == "win32":
            raise Exception("You have to be fucking kidding me")
