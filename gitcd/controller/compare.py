from gitcd.controller import Base
from gitcd.git.branch import Branch
from gitcd.git.tag import Tag
from gitcd.git.remote import Remote


class Compare(Base):

    def compare(
        self,
        currentBranch: Branch,
        branch: [Branch, Tag],
        remote: Remote
    ) -> bool:
        return remote.compare(currentBranch, branch)
