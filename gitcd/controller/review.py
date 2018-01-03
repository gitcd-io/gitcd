from gitcd.controller import Base
from gitcd.git.branch import Branch
from gitcd.git.remote import Remote


class Review(Base):

    def openPullRequest(self) -> bool:

        return True
