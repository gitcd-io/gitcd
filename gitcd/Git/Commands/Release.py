from gitcd.Git.Command import Command
import time


class Release(Command):

    def execute(self, dummy: str):
        self.interface.header("gitcd release")

        origin = self.getOrigin()

        self.cli.execute("git checkout %s" % (self.config.getMaster()))
        self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))

        # push new tag
        if self.config.getVersionType() == 'manual':
            tagNumber = self.interface.askFor(
                "Whats the current tag number you want to deliver?")
        else:
            tagNumber = time.strftime(self.config.getVersionScheme())

        tagMessage = self.interface.askFor(
            "What message your new tag should have?")
        # escape double quotes for shell command
        tagMessage = tagMessage.replace('"', '\\"')
        self.cli.execute(
            'git tag -a -m "%s" %s%s' % (
                tagMessage, self.config.getString(self.config.getTag()),
                tagNumber
            )
        )
        self.cli.execute(
            "git push %s %s%s"
            % (origin, self.config.getString(self.config.getTag()), tagNumber)
        )
