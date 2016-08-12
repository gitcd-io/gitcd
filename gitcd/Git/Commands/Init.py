from gitcd.Git.Command import Command


class Init(Command):

    # no special subcommands, only run which is meant to be default

    def run(self, dummy: str):
        self.config.setMaster(
            self.interface.askFor(
                "Branch name for production releases?",
                False,
                self.config.getMaster()
            )
        )

        featureDefault = self.config.getFeature()
        if featureDefault is None:
            featureDefault = '<none>'
        self.config.setFeature(
            self.interface.askFor(
                "Branch name for feature development?",
                False,
                featureDefault
            )
        )

        testDefault = self.config.getTest()
        if testDefault is None:
            testDefault = '<none>'
        self.config.setTest(
            self.interface.askFor(
                "Branch name for test releases?",
                False,
                testDefault
            )
        )

        tagDefault = self.config.getTag()
        if tagDefault is None:
            tagDefault = '<none>'
        self.config.setTag(
            self.interface.askFor(
                "Version tag prefix?",
                False,
                tagDefault
            )
        )

        # ask for version type, manual or date
        versionType = self.interface.askFor(
            "Version type? You can either set your tag number" +
            " manually or generate it by date.",
            ['manual', 'date'],
            self.config.getVersionType()
        )
        self.config.setVersionType(versionType)

        # if type is date ask for scheme
        if versionType == 'date':
            versionScheme = self.interface.askFor(
                "Scheme for your date-tag?" +
                " Year: %Y / Month: %m  / Day: %d /" +
                " Hour: %H / Minute: %M / Second: %S",
                '%Y.%m.%d%H%M',
                self.config.getVersionScheme()
            )
        else:
            # you'll be asked for it while a release
            versionScheme = None

        # pass version scheme to config
        self.config.setVersionScheme(versionScheme)

        self.configPersonal.setToken(
            self.interface.askFor(
                "Your personal Github token?",
                False,
                self.configPersonal.getToken()
            )
        )

        self.configPersonal.write()
        self.config.write()
