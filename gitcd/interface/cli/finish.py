from gitcd.interface.cli.abstract import BaseCommand
from gitcd.git.branch import Branch


class Finish(BaseCommand):

    def run(self, branch: Branch):
        remote = self.getRemote()

        testBranch = self.config.getTest()
        masterBranch = self.config.getMaster()

        if branch.getName() == masterBranch:
            # maybe i should use recursion here
            # if anyone passes master again, i wouldnt notice
            branch = Branch('%s%s' % (
                branch.getName(),
                self.interface.askFor(
                    "You passed your master branch name as feature branch,\
                    please give a different name."
                )
            ))

        if testBranch:
            if branch.getName().startswith(testBranch):
                # maybe i should use recursion here
                # if anyone passes master again, i wouldnt notice
                branch = Branch('%s%s' % (
                    branch.getName(),
                    self.interface.askFor(
                        "You passed your test branch name as feature branch,\
                        please give a different branch."
                    )
                ))
        self.checkRepository()
        self.checkBranch(remote, branch)

        master = Branch(masterBranch)

        self.mergeWithRetry(remote, master, branch)

        deleteFeatureBranch = self.interface.askFor(
            "Delete your feature branch?", ["yes", "no"], "yes"
        )

        if deleteFeatureBranch == "yes":
            # delete feature branch remote and locally
            remote.delete(branch)
            branch.delete()
