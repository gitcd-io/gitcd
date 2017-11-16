import os

from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.repository import Repository
# from gitcd.git.remote import Remote
# from gitcd.git.branch import Branch
# from gitcd.git.tag import Tag

from pprint import pprint

class Clean(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd clean')
        print(os.getcwd())
        repository = Repository(os.getcwd())
        remotes = repository.getRemotes()
        branches = repository.getBranches()
        tags = repository.getTags()

        pprint(remotes)
        pprint(branches)
        pprint(tags)

        # for branch in branches:
        #     deleteBranch = True
        #     for remote in remotes:
        #         if remote.hasBranch(branch):
        #             deleteBranch = False

        #     if deleteBranch:
        #         branch.delete()

        # for tag in tags:
        #     deleteTag = True
        #     for remote in remotes:
        #         if remote.hasTag(tag):
        #             deleteTag = False

        #     if deleteTag:
        #         tag.delete()