from gitcd.interface.cli.abstract import BaseCommand

from gitcd.controller.compare import Compare as CompareController

from gitcd.git.branch import Branch
from gitcd.git.tag import Tag


class Compare(BaseCommand):

    def getDefaultBranch(self) -> [Branch, Tag]:
        controller= CompareController()
        repository = controller.getRepository()
        return repository.getLatestTag()

    def getRequestedBranch(self, branch: str) -> [Branch, Tag]:
        masterBranch = self.config.getMaster()
        tagPrefix = self.config.getTag()
        if branch.startswith(tagPrefix):
            branch = Tag(branch)
        else:
            branch = Branch(branch)

        return branch

    def run(self, branch: [Branch, Tag]):
        self.interface.header('git-cd compare')

        remote = self.getRemote()
        controller= CompareController()
        currentBranch = controller.getCurrentBranch()
        repository = controller.getRepository()

        if repository.hasUncommitedChanges():
            abort = self.interface.askFor(
                "You currently have uncomitted changes." +
                " Do you want me to abort and let you commit first?",
                ["yes", "no"],
                "yes"
            )

            if abort == "yes":
                return False

        # check remote existence
        if type(branch) is Branch and not remote.hasBranch(branch):
            pushFeatureBranch = self.interface.askFor(
                "Your feature branch (%s) does not exists on origin. Do you want me to push it remote?" % (branch.getName()), ["yes", "no"], "yes"
            )

            if pushFeatureBranch == "yes":
                remote.push(branch)

        if type(branch) is Tag and not remote.hasTag(branch):
            pushFeatureBranch = self.interface.askFor(
                "Your tag (%s) does not exists on origin. Do you want me to push it remote?" % (branch.getName()), ["yes", "no"], "yes"
            )

            if pushFeatureBranch == "yes":
                remote.push(branch)


        # check behind origin
        if remote.isBehind(branch):

            pushFeatureBranch = self.interface.askFor(
                "Your feature branch is ahead the origin/branch." +
                " Do you want me to push the changes?",
                ["yes", "no"],
                "yes"
            )

            if pushFeatureBranch == "yes":
                remote.push(branch)

        controller.compare(currentBranch, branch, remote)
