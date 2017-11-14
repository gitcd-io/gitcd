import os

from gitcd.interface.cli.abstract import BaseCommand


class Init(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd init')

        self.config.setMaster(
            self.cli.askFor(
                "Branch name for production releases?",
                False,
                self.config.getMaster()
            )
        )

        featureDefault = self.config.getFeature()
        if featureDefault is None:
            featureDefault = '<none>'
        self.config.setFeature(
            self.cli.askFor(
                "Branch name for feature development?",
                False,
                featureDefault
            )
        )

        testDefault = self.config.getTest()
        if testDefault is None:
            testDefault = '<none>'
        self.config.setTest(
            self.cli.askFor(
                "Branch name for test releases?",
                False,
                testDefault
            )
        )

        tagDefault = self.config.getTag()
        if tagDefault is None:
            tagDefault = '<none>'
        self.config.setTag(
            self.cli.askFor(
                "Version tag prefix?",
                False,
                tagDefault
            )
        )

        # ask for version type, manual or date
        versionType = self.cli.askFor(
            "Version type? You can either set your tag number" +
            " manually, read it from a version file or generate it by date.",
            ['manual', 'date', 'file'],
            self.config.getVersionType()
        )
        self.config.setVersionType(versionType)

        # if type is date ask for scheme
        if versionType == 'date':
            versionScheme = self.cli.askFor(
                "Scheme for your date-tag?" +
                " Year: %Y / Month: %m  / Day: %d /" +
                " Hour: %H / Minute: %M / Second: %S",
                '%Y.%m.%d%H%M',
                self.config.getVersionScheme()
            )
        elif versionType == 'file':
            versionScheme = self.cli.askFor(
                "From what file do you want to load your version?",
                False,
                self.config.getVersionScheme()
            )
            if not os.path.isfile(versionScheme):
                self.cli.error(
                    'Could not find your version file, ' +
                    'stick back to manual tag number!'
                )
                versionScheme = None
                versionType = 'manual'
        else:
            # you'll be asked for it while a release
            versionScheme = None

        extraReleaseCommandDefault = self.config.getExtraReleaseCommand()
        if extraReleaseCommandDefault is None:
            extraReleaseCommandDefault = '<none>'
        self.config.setExtraReleaseCommand(
            self.cli.askFor(
                "Do you want to execute some additional" +
                "commands after a release?",
                False,
                extraReleaseCommandDefault
            )
        )

        # pass version scheme to config
        self.config.setVersionScheme(versionScheme)

        self.config.write()
