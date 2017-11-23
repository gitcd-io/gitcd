from packaging import version

from gitcd.controller import Base

from gitcd.git.repository import Repository

from gitcd.package import Package


class Upgrade(Base):

    localVersion = 0
    pypiVersion = 0

    def getLocalVersion(self) -> str:
        package = Package()
        self.localVersion = package.getLocalVersion()

        return self.localVersion

    def getPypiVersion(self) -> str:
        package = Package()
        self.pypiVersion = package.getPypiVersion()

        return self.pypiVersion

    def isUpgradable(self) -> bool:
        if version.parse(self.localVersion) < version.parse(self.pypiVersion):
            return True
        return False

    def upgrade(self) -> bool:
        package = Package()
        package.upgrade()

        return True
