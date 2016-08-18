import requests
import json

from gitcd.Git.Command import Command
from gitcd.Exceptions import GitcdGithubApiException

from pprint import pprint
import sys

class Status(Command):

    def execute(self, branch: str):
        featureBranch = self.getFeatureBranch(branch)
        self.interface.header("see status for branch %s" % featureBranch)

        origin = self.getOrigin()
        master = self.config.getMaster()
        repo = self.getRepository(origin)
        username = self.getUsername(origin)
        token = self.getTokenOrAskFor()

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

            pprint(response)
            sys.exit(1)

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
