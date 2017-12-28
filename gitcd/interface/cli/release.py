from gitcd.interface.cli.abstract import BaseCommand
from gitcd.controller.release import Release as ReleaseController
from gitcd.git.branch import Branch
from gitcd.git.remote import Remote


class Release(BaseCommand):

    def run(self, branch: Branch):
        self.interface.header('git-cd release')

        remote = self.getRemote()
        masterBranch = Branch(self.config.getMaster())

        controller = ReleaseController()
        controller.checkout(remote, masterBranch)

        version = controller.getVersion()
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

        controller.release(version, message, remote)

        return True
