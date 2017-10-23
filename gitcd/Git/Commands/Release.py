from gitcd.Git.Command import Command
from gitcd.Exceptions import GitcdVersionFileNotFoundException
import time
import os


class Release(Command):

    def execute(self, dummy: str):
        self.interface.header("gitcd release")

        origin = self.getOrigin()

        self.cli.execute("git checkout %s" % (self.config.getMaster()))
        self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))

        # push new tag
        askForVersion = True
        if self.config.getVersionType() == 'file':
            try:
                tagNumber = self.readVersionFile(
                    self.config.getVersionScheme()
                )
                askForVersion = False
            except GitcdVersionFileNotFoundException:
                self.interface.info(
                    'Could not load version file "%s", ' +
                    'please pass a version manually.'
                )
                askForVersion = True
        elif self.config.getVersionType == 'date':
            tagNumber = time.strftime(self.config.getVersionScheme())

        if askForVersion is True:
            tagNumber = self.interface.askFor(
                "Whats the current tag number you want to deliver?")

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

    def readVersionFile(self, versionFile: str):
        if not os.path.isfile(versionFile):
            raise GitcdVersionFileNotFoundException('Version file not found!')
        with open(versionFile, 'r') as f:
            return f.read().strip
