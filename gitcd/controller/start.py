from gitcd.controller import Base
from gitcd.git.remote import Remote
from gitcd.git.branch import Branch


class Start(Base):

    def start(self, feature: Branch, remote: Remote) -> bool:
        remote.createFeature(feature)
