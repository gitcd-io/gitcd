from gitcd.controller import Base
from gitcd.git.branch import Branch
from gitcd.git.remote import Remote


class Finish(Base):

    def mergeIntoMaster(self, branch: Branch, remote: Remote) -> bool:
        master = Branch(self.config.getMaster())
        remote.merge(master, branch)

        return True
