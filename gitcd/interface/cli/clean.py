
from gitcd.interface.cli.abstract import BaseCommand


from gitcd.controller.clean import Clean as CleanController

from pprint import pprint
import sys


class Clean(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd clean')

        controller = CleanController()

        branchesToDelete = controller.getBranchesToDelete()

        self.interface.writeOut('Branches to delete')

        if len(branchesToDelete) == 0:
            self.interface.ok('  - no branches to delete')

        for branchToDelete in branchesToDelete:
            self.interface.red("  - %s" % branchToDelete.getName())

        tagsToDelete = controller.getTagsToDelete()

        self.interface.writeOut('Tags to delete')

        if len(branchesToDelete) == 0:
            self.interface.ok('  - no tags to delete')

        for tagToDelete in tagsToDelete:
            self.interface.red("  - %s" % tagToDelete.getName())

        self.interface.writeOut('')
        if len(branchesToDelete) == 0 and len(tagsToDelete) == 0:
            self.interface.ok('Nice, your local repository is clean already.')
            return True

        delete = self.interface.askFor(
            'Do you want me to delete those branches and tags locally?',
            ['yes', 'no'],
            'yes'
        )
        if delete == 'yes':
            controller.deleteBranches(branchesToDelete)
            controller.deleteTags(tagsToDelete)

        return True
