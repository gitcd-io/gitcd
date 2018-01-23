from gitcd.interface.cli.abstract import BaseCommand
from gitcd.git.branch import Branch

from gitcd.app.release import Release as ReleaseHelper


class Release(BaseCommand):

    def run(self, branch: Branch):
        remote = self.getRemote()
        masterBranch = Branch(self.config.getMaster())

        releaseHelper = ReleaseHelper()

        releaseHelper.checkout(remote, masterBranch)

        version = releaseHelper.getVersion()
        if version is False:
            version = self.interface.askFor(
                "Whats the current version number you want to release?")

        message = self.interface.askFor(
            "What message your new release should have?")
        # escape double quotes for shell command
        message = message.replace('"', '\\"')

        version = '%s%s' % (
            self.config.getString(self.config.getTag()),
            version
        )

        releaseHelper.release(version, message, remote)

        return True
