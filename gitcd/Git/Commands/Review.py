import requests
import json

from gitcd.Git.Command import Command
from gitcd.Exceptions import GitcdGithubApiException


class Review(Command):

    def execute(self, branch: str):
        self.interface.header("open a pull request on github")

        featureBranch = self.getFeatureBranch(branch)
        origin = self.getOrigin()
        master = self.config.getMaster()
        repo = self.getRepository(origin)
        username = self.getUsername(origin)
        token = self.getTokenOrAskFor()

        if not self.checkBranch(origin, featureBranch):
            return False

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
                jsonResponse = response.json()
                message = jsonResponse['errors'][0]['message']
                raise GitcdGithubApiException(
                    "Open a pull request failed with message: %s" % (
                        message
                    )
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
