import os

from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.repository import Repository

from gitcd.controller.clean import Clean as CleanController

from pprint import pprint
import sys

class Clean(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd clean')

        repository = Repository(os.getcwd())
        controller = CleanController(repository)

        branchesToDelete = controller.getBranchesToDelete()

        self.cli.writeOut('Branches to delete')

        if len(branchesToDelete) == 0:
            self.cli.ok('  - no branches to delete')

        for branchToDelete in branchesToDelete:
            self.cli.warning("  - <%s>" % branchToDelete.getName())


        tagsToDelete = controller.getTagsToDelete()

        self.cli.writeOut('Tags to delete')

        if len(branchesToDelete) == 0:
            self.cli.ok('  - no tags to delete')

        for tagToDelete in tagsToDelete:
            self.cli.warning("  - <%s>" % tagToDelete.getName())

        if len(branchesToDelete) == 0 and len(tagsToDelete) == 0:
            self.cli.info('Nice, your local repository is clean already.')
            return True

        delete = self.cli.askFor(
            "Do you want me to delete those branches and tags locally?",
            ["yes", "no"],
            "yes"
        )
        if delete == 'yes':
            controller.deleteBranches(branchesToDelete)
            controller.deleteTags(tagsToDelete)

        return True
