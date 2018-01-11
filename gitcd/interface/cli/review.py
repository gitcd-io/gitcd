from gitcd.interface.cli.abstract import BaseCommand

from gitcd.controller.review import Review as ReviewController

from gitcd.git.branch import Branch

from gitcd.exceptions import GitcdNoFeatureBranchException
from gitcd.exceptions import GitcdGithubApiException


class Review(BaseCommand):

    def run(self, branch: Branch):
        remote = self.getRemote()
        controller = ReviewController()
        repository = controller.getRepository()
        master = Branch(self.config.getMaster())
        # ensure a token is set
        token = self.getTokenOrAskFor()

        self.checkRepository()
        self.checkBranch(remote, branch)

        self.interface.warning("Opening pull-request")

        title = self.interface.askFor("Pull-Request title?")
        body = self.interface.askFor("Pull-Request body?")
        remote.openPullRequest(title, body, branch, master)
