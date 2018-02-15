from typing import Union
import time
import os
import simpcli

from gitcd.git.repository import Repository
from gitcd.git.branch import Branch
from gitcd.git.remote import Remote
from gitcd.git.tag import Tag

from gitcd.exceptions import GitcdVersionFileNotFoundException
from gitcd.app import App


class Release(App):

    def checkout(self, remote: Remote, branch: Branch) -> bool:
        repository = Repository()
        repository.checkoutBranch(branch)
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
        extraCommand = self.config.getExtraReleaseCommand()
        if extraCommand is not None:
            cli = simpcli.Command(True)
            cli.execute(
                extraCommand
            )

        return True
