from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.branch import Branch

import time


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

        # check if pr is open already
        pr = remote.getGitWebIntegration()
        self.getTokenOrAskFor(pr.getTokenSpace())
        prInfo = pr.status(branch, sourceRemote)
        if 'url' in prInfo:
            self.interface.info(
                'Pull request is already open. ' +
                'I\'ll be so nice and open it for you in 3 seconds...'
            )
            self.interface.writeOut(
                'Press ctrl+c if you dont like me to.'
            )
            time.sleep(3)
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
