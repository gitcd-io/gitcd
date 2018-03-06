from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.branch import Branch


class Review(BaseCommand):

    def run(self, branch: Branch):
        remote = self.getRemote()
        master = Branch(self.config.getMaster())

        self.checkRepository()
        self.checkBranch(remote, branch)

        self.interface.warning("Opening pull-request")

        title = self.interface.askFor("Pull-Request title?")
        body = self.interface.askFor("Pull-Request body?")
        pr = remote.getGitWebIntegration()
        # ensure a token is set for this remote
        self.getTokenOrAskFor(pr.getTokenSpace())
        pr.open(title, body, branch, master)
