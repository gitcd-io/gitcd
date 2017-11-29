from gitcd.controller import Base
from gitcd.git.branch import Branch
from gitcd.git.remote import Remote

class Finish(Base):

    def mergeIntoMaster(self, branch: Branch, remote: Remote) -> bool:
        self.verboseCli.execute("git checkout %s" % (self.config.getMaster()))
        self.cli.execute("git pull %s %s" % (remote.getName(), self.config.getMaster()))
        self.cli.execute("git merge %s/%s" % (remote.getName(), branch.getName()))
        self.cli.execute("git push %s %s" % (remote.getName(), self.config.getMaster()))

        return True
