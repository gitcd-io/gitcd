from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.branch import Branch


class Review(BaseCommand):

    def run(self, branch: Branch):
        remote = self.getRemote("as target remote")
        sourceRemote = None
        if self.hasMultipleRemotes() is True:
            sourceRemote = self.getRemote("as source remote")
            if sourceRemote.getUrl() == remote.getUrl():
                sourceRemote = None

        master = Branch(self.config.getMaster())

        self.checkRepository()

        if sourceRemote is None:
            self.checkBranch(remote, branch)
        else:
            self.checkBranch(sourceRemote, branch)

        self.interface.warning("Opening pull-request")

        # check if pr is open already
        pr = remote.getGitWebIntegration()
        self.getTokenOrAskFor(pr.getTokenSpace())
        prInfo = pr.status(branch, sourceRemote)
        if prInfo is not None and 'url' in prInfo:
            openPr = self.interface.askFor(
                'Pull request is already open. ' +
                'Should i open it in your browser?',
                ["yes", "no"],
                "yes"
            )

            if openPr == "yes":
                pr.openBrowser(prInfo['url'])

            return True

        # ask for title and body
        title = self.interface.askFor(
            'Pull-Request title?',
            False,
            branch.getName()
        )

        body = self.interface.askFor("Pull-Request body?")
        # go on opening pr
        pr.open(title, body, branch, master, sourceRemote)
