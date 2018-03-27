from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.branch import Branch


class Review(BaseCommand):

    def run(self, branch: Branch):
        remote = self.getRemote()
        sourceRemote = None
        if self.hasMultipleRemotes() is True:
            sourceRemote = self.getRemote()
            if sourceRemote.getUrl() == remote.getUrl():
                sourceRemote = None

        master = Branch(self.config.getMaster())

        self.checkRepository()

        if sourceRemote is None:
            self.checkBranch(remote, branch)
        else:
            self.checkBranch(sourceRemote, branch)

        self.interface.warning("Opening pull-request")

        title = self.interface.askFor(
            'Pull-Request title?',
            False,
            branch.getName()
        )

        body = self.interface.askFor("Pull-Request body?")
        pr = remote.getGitWebIntegration()
        # ensure a token is set for this remote
        self.getTokenOrAskFor(pr.getTokenSpace())
        pr.open(title, body, branch, master, sourceRemote)
