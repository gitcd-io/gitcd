import requests
import json

from gitcd.Git.Command import Command
from gitcd.Exceptions import GitcdNoDevelopmentBranchDefinedException
from gitcd.Exceptions import GitcdGithubApiException


class Feature(Command):

    def getSubcommands(self):
        return [
            'start',
            'test',
            'review',
            'finish'
        ]

    def start(self, branch: str):
        self.interface.header("gitcd feature start")

        origin = self.getOrigin()
        featurePrefix = self.config.getFeature()
        testBranch = self.config.getTest()
        masterBranch = self.config.getMaster()
        # ask for branch if nothing passed
        if branch == "*":
            branch = self.interface.askFor(
                "Name for your new feature-branch? (without %s prefix)"
                % self.config.getString(self.config.getFeature())
            )

        if testBranch is not None:
            if branch == testBranch:
                # maybe i should use recursion here
                # if anyone passes develop again, i wouldnt notice
                branch = self.interface.askFor(
                    "You passed your test branch name as feature branch,\
                    please give a different name."
                )

        if branch == masterBranch:
            # maybe i should use recursion here
            # if anyone passes master again, i wouldnt notice
            branch = self.interface.askFor(
                "You passed your master branch name as feature branch,\
                please give a different name."
            )

        if featurePrefix is not None:
            if branch.startswith(featurePrefix):
                fixFeatureBranch = self.interface.askFor(
                    "Your feature branch already starts" +
                    " with your feature prefix," +
                    " should i remove it for you?",
                    ["yes", "no"],
                    "yes"
                )

                if fixFeatureBranch == "yes":
                    branch = branch.replace(self.config.getFeature(), "")

        featureBranch = "%s%s" % (
            self.config.getString(self.config.getFeature()),
            branch
        )

        self.cli.execute(
            "git checkout %s" % (self.config.getMaster())
        )
        self.cli.execute(
            "git pull %s %s" % (origin, self.config.getMaster())
        )
        self.cli.execute(
            "git checkout -b %s" % (featureBranch)
        )
        self.cli.execute(
            "git push %s %s" % (origin, featureBranch)
        )
        self.cli.execute(
            "git branch --set-upstream-to %s/%s" % (origin, featureBranch)
        )

    def checkBranch(self, origin: str, branch: str):
        # uncomitted changes
        if self.hasUncommitedChanges():
            abort = self.interface.askFor(
                "You currently have uncomitted changes." +
                " Do you want me to abort and let you commit first?",
                ["yes", "no"],
                "yes"
            )

            if abort == "yes":
                return False

        # will fail if the branch does not exists locally
        self.cli.execute("git checkout %s" % (branch))

        # check remote existence
        if not self.remoteHasBranch(origin, branch):
            pushFeatureBranch = self.interface.askFor(
                "Your feature branch does not exists on origin." +
                " Do you want me to push it remote?", ["yes", "no"], "yes"
            )

            if pushFeatureBranch == "yes":
                self.cli.execute(
                    "git push %s %s" % (origin, branch)
                )

        # check behind origin
        if self.isBehindOrigin(origin, branch):

            pushFeatureBranch = self.interface.askFor(
                "Your feature branch is behind the origin/branch." +
                " Do you want me to push the changes?",
                ["yes", "no"],
                "yes"
            )

            if pushFeatureBranch == "yes":
                self.cli.execute(
                    "git push %s %s" % (origin, branch)
                )

        return True

    def test(self, branch: str):
        try:
            self.interface.header("gitcd feature test")

            origin = self.getOrigin()
            developmentBranch = self.getDevelopmentBranch()
            featureBranch = self.getFeatureBranch(branch)

            if not self.checkBranch(origin, featureBranch):
                return False

            self.cli.execute("git checkout %s" % (developmentBranch))
            self.cli.execute("git pull %s %s" % (origin, developmentBranch))
            self.cli.execute("git merge %s/%s" % (origin, featureBranch))
            self.cli.execute("git push %s %s" % (origin, developmentBranch))

        except GitcdNoDevelopmentBranchDefinedException as e:
            self.interface.writeOut("gitcd error: %s" % (format(e)))

    def review(self, branch: str):
        self.interface.header("open a pull request on github")

        featureBranch = self.getFeatureBranch(branch)
        origin = self.getOrigin()
        master = self.config.getMaster()
        repo = self.getRepository(origin)
        username = self.getUsername(origin)
        token = self.configPersonal.getToken()

        if isinstance(token, str):
            url = "https://api.github.com/repos/%s/%s/pulls" % (username, repo)
            title = self.interface.askFor("Pull-Request title?")
            body = self.interface.askFor("Pull-Request body?")

            data = {
                "title": title,
                "body": body,
                "head": featureBranch,
                "base": master
            }

            self.interface.warning("Opening pull-request on %s" % (url))

            headers = {'Authorization': 'token %s' % token}
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(data),
            )
            if response.status_code != 201:
                # todo better handling of errors here, ie. pull-request already
                # existss
                raise GitcdGithubApiException(
                    "Could not create a pull request," +
                    " please create it manually."
                )

            defaultBrowser = self.getDefaultBrowserCommand()
            self.cli.execute("%s %s" % (
                defaultBrowser,
                response.json()["html_url"]
            ))

        else:
            defaultBrowser = self.getDefaultBrowserCommand()
            self.cli.execute("%s https://github.com/%s/%s/compare/%s...%s" % (
                defaultBrowser,
                username,
                repo,
                master,
                featureBranch
            ))

    def finish(self, branch: str):
        self.interface.header("gitcd feature finish")

        origin = self.getOrigin()

        featureBranch = self.getFeatureBranch(branch)

        if not self.checkBranch(origin, featureBranch):
            return False

        self.cli.execute("git checkout %s" % (self.config.getMaster()))
        self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))
        self.cli.execute("git merge %s/%s" % (origin, featureBranch))
        self.cli.execute("git push %s %s" % (origin, self.config.getMaster()))

        deleteFeatureBranch = self.interface.askFor(
            "Delete your feature branch?", ["yes", "no"], "yes"
        )

        if deleteFeatureBranch == "yes":
            # delete feature branch remote and locally
            self.cli.execute("git push %s :%s" % (origin, featureBranch))
            self.cli.execute("git branch -D %s" % (featureBranch))
