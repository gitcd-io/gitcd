from gitcd.controller import Base

from gitcd.git.branch import Branch
from gitcd.git.tag import Tag

from pprint import pprint

class Clean(Base):

    def getBranchesToDelete(self) -> [Branch]:
        remotes = self.repository.getRemotes()
        branches = self.repository.getBranches()
        currentBranch = self.repository.getCurrentBranch()

        branchesToDelete = []

        for branch in branches:
            deleteBranch = True
            for remote in remotes:
                if remote.hasBranch(branch):
                    deleteBranch = False

            if deleteBranch:
                branchesToDelete.append(branch)
        
        return branchesToDelete

    def deleteBranches(self, branches: [Branch] = []) -> bool:
        for branch in branches:
            branch.delete()

        return True

    def getTagsToDelete(self) -> [Tag]:
        remotes = self.repository.getRemotes()
        tags = self.repository.getTags()
        
        tagsToDelete = []
        for tag in tags:
            deleteTag = True
            for remote in remotes:
                if remote.hasTag(tag):
                    deleteTag = False

            if deleteTag:
                tagsToDelete.append(tag)

        return tagsToDelete

    def deleteTags(self, tags: [Tag]) -> bool:
        for tag in tags:
            tag.delete()

        return True