from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.branch import Branch


class Refresh(BaseCommand):

    updateRemote = True

    def run(self, branch: Branch):
        remote = self.getRemote()
        master = Branch(self.config.getMaster())

        if branch.getName() == master.getName():
            # maybe i should use recursion here
            # if anyone passes master again, i wouldnt notice
            branch = Branch('%s%s' % (
                branch.getName(),
                self.interface.askFor(
                    "You passed your master branch name as feature branch,\
                    please give a different branch."
                )
            ))

        remote.merge(branch, master)
