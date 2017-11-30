from gitcd.git import Git

from pprint import pprint


class Branch(Git):

    name = 'master'

    def __init__(self, name: str):
        self.name = name

    def getName(self) -> str:
        return self.name

    def isMaster(self) -> bool:
        return self.name == self.config.getMaster()

    def isTest(self) -> bool:
        testPrefix = self.config.getTest()
        if not testPrefix:
            return False

        return self.name.startswith(testPrefix)

    def isFeature(self) -> bool:
        if self.isMaster() or self.isTest():
            return False

        if self.config.getFeature():
            return self.name.startswith(self.config.getFeature())
        return True

    def delete(self) -> bool:
        output = self.verboseCli.execute("git branch -D %s" % (self.name))
        if output is False:
            return False
        return True

    # def deleteRemote(self, remote) -> bool:
    #     output = self.verboseCli.execute("git push %s :%s" % (remote.getName(), self.name))
    #     if output is False:
    #         return False
    #     return True

    # def push(self, remote) -> bool:
    #     self.cli.execute(
    #         "git push %s %s" % (remote.getName(), self.name)
    #     )

    #     return True

    # def isAhead(self, remote) -> bool:
    #     output = self.cli.execute(
    #         "git log %s/%s..%s" % (remote.getName(), self.name, self.name)
    #     )
    #     if not output:
    #         return False

    #     return True

    # def merge(self, branch, remote) -> bool:
    #     self.verboseCli.execute("git checkout %s" % (self.name))
    #     self.verboseCli.execute("git pull %s %s" % (remote.getName(), self.config.getMaster()))
    #     self.verboseCli.execute("git merge %s/%s" % (remote.getName(), branch.getName()))
    #     remote.push(self)
