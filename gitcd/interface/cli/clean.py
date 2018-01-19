from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.branch import Branch

from gitcd.app.clean import Clean as CleanHelper


class Clean(BaseCommand):

    updateRemotes = True

    def run(self, branch: Branch):
        helper = CleanHelper()

        branchesToDelete = helper.getBranchesToDelete()

        self.interface.writeOut('Branches to delete')

        if len(branchesToDelete) == 0:
            self.interface.ok('  - no branches to delete')

        for branchToDelete in branchesToDelete:
            self.interface.red("  - %s" % branchToDelete.getName())

        self.interface.writeOut('')
        if len(branchesToDelete) == 0:
            self.interface.ok('Nice, your local repository is clean already.')
            return True

        delete = self.interface.askFor(
            'Do you want me to delete those branches locally?',
            ['yes', 'no'],
            'yes'
        )
        if delete == 'yes':
            helper.deleteBranches(branchesToDelete)

        return True
