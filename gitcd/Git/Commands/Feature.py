import time
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
            'finish',
            'release'
        ]

    def start(self, branch: str):
        self.interface.header("gitcd feature start")

        origin = self.getOrigin()

        # ask for branch if nothing passed
        if branch == "*":
            branch = self.interface.askFor(
                "Name for your new feature-branch? (without %s prefix)" %
                self.config.getFeature())

        if branch.startswith(self.config.getFeature()):
            fixFeatureBranch = self.interface.askFor(
                "Your feature branch already starts with your feature prefix,\
                should i remove it for you?", [
                    "yes", "no"], "yes")

            if fixFeatureBranch == "yes":
                branch = branch.replace(self.config.getFeature(), "")

        featureBranch = "%s%s" % (self.config.getFeature(), branch)

        self.cli.execute("git checkout %s" % (self.config.getMaster()))
        self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))
        self.cli.execute("git checkout -b %s" % (featureBranch))
        self.cli.execute("git push %s %s" % (origin, featureBranch))
        self.cli.execute(
            "git branch --set-upstream-to %s/%s" %
            (origin, featureBranch))

    def test(self, branch: str):
        try:
            self.interface.header("gitcd feature test")

            origin = self.getOrigin()
            developmentBranch = self.getDevelopmentBranch()

            featureBranch = self.getFeatureBranch(branch)

            self.cli.execute("git checkout %s" % (developmentBranch))
            self.cli.execute("git pull %s %s" % (origin, developmentBranch))
            self.cli.execute("git merge %s" % (featureBranch))
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
                    "Could not create a pull request,\
                    please create it manually.")

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

        self.cli.execute("git checkout %s" % (self.config.getMaster()))
        self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))
        self.cli.execute("git merge %s" % (featureBranch))
        self.cli.execute("git push %s %s" % (origin, self.config.getMaster()))

        deleteFeatureBranch = self.interface.askFor(
            "Delete your feature branch?", ["yes", "no"], "yes")

        if deleteFeatureBranch == "yes":
            # delete feature branch locally and remote
            self.cli.execute("git branch -D %s" % (featureBranch))
            self.cli.execute("git push %s :%s" % (origin, featureBranch))
