from typing import Union
import time
import os

from gitcd.controller import Base
from gitcd.git.branch import Branch
from gitcd.git.remote import Remote
from gitcd.git.tag import Tag

from gitcd.exceptions import GitcdVersionFileNotFoundException


class Release(Base):

    def checkout(self, remote: Remote, branch: Branch) -> bool:
        self.repository.checkoutBranch(branch)
        remote.pull(branch)
        return True

    def readVersionFile(self, versionFile) -> Union[str, bool]:
        if not os.path.isfile(versionFile):
            raise GitcdVersionFileNotFoundException('Version file not found!')
        with open(versionFile, 'r') as f:
            return f.read().strip()

    def getVersion(self) -> Union[str, bool]:
        if self.config.getVersionType() == 'file':
            try:
                return self.readVersionFile(
                    self.config.getVersionScheme()
                )
            except GitcdVersionFileNotFoundException:
                return False
        elif self.config.getVersionType() == 'date':
            return time.strftime(self.config.getVersionScheme())

        return False

    def release(self, version: str, message: str, remote: Remote) -> bool:
        tag = Tag(version)
        tag.create(message)
        remote.push(tag)

        return True
