import os

from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.repository import Repository

from pprint import pprint

class Clean(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd clean')

        repository = Repository(os.getcwd())
        remotes = repository.getRemotes()
        branches = repository.getBranches()
        tags = repository.getTags()
        currentBranch = repository.getCurrentBranch()

        for branch in branches:
            deleteBranch = True
            for remote in remotes:
                if remote.hasBranch(branch):
                    deleteBranch = False

            if deleteBranch:
                print(branch.getName())
                print(currentBranch.getName())
                if branch.getName() == currentBranch.getName():
                    currentBranch = repository.checkoutBranch(self.config.getMaster())
                branch.delete()

        for tag in tags:
            deleteTag = True
            for remote in remotes:
                if remote.hasTag(tag):
                    deleteTag = False

            if deleteTag:
                tag.delete()
