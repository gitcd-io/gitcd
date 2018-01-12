from gitcd.controller import Base
from gitcd.git.branch import Branch

from gitcd.exceptions import GitcdNoDevelopmentBranchDefinedException


class Test(Base):

    def getDevelopmentBranches(self) -> [Branch]:
        branches = self.repository.getBranches()
        developmentBranches = []
        for branch in branches:
            if branch.isTest():
                developmentBranches.append(branch)

        if len(developmentBranches) < 1:
            raise GitcdNoDevelopmentBranchDefinedException(
                "No development branch found"
            )
        return developmentBranches
