from gitcd.interface.cli.abstract import BaseCommand

from gitcd.controller.review import Review as ReviewController

from gitcd.git.branch import Branch

from gitcd.exceptions import GitcdNoFeatureBranchException
from gitcd.exceptions import GitcdGithubApiException


class Review(BaseCommand):

    def getTokenOrAskFor(self):
        token = self.configPersonal.getToken()
        if token is None:
            token = self.interface.askFor(
                "Your personal Github token?",
                False,
                token
            )
            self.configPersonal.setToken(token)
            self.configPersonal.write()
        return token

    def run(self, branch: Branch):
        self.interface.header('git-cd review')

        remote = self.getRemote()
        controller = ReviewController()
        repository = controller.getRepository()
        master = Branch(self.config.getMaster())
        # ensure a token is set
        token = self.getTokenOrAskFor()

        # check if its a feature branch
        if not branch.isFeature():
            raise GitcdNoFeatureBranchException(
                "Your current branch is not a valid feature branch." +
                " Checkout a feature branch or pass one as param."
            )

        # check if repo has uncommited changes
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
        if not remote.hasBranch(branch):
            pushFeatureBranch = self.interface.askFor(
                "Your feature branch does not exists on origin." +
                " Do you want me to push it remote?", ["yes", "no"], "yes"
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


        self.interface.warning("Opening pull-request")

        title = self.interface.askFor("Pull-Request title?")
        body = self.interface.askFor("Pull-Request body?")
        remote.openPullRequest(title, body, branch, master)
