from gitcd.controller import Base
from gitcd.git.remote import Remote


class Start(Base):

    def start(self, feature: str, remote: Remote) -> bool:
        remote.createFeature(feature)
