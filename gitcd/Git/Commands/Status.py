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

            data = {
                "state": 'open',
                "head": featureBranch,
                "base": master
            }

            self.interface.warning("Fetch pull-request infos on %s" % (url))

            headers = {'Authorization': 'token %s' % token}
            response = requests.get(
                url,
                headers=headers,
                params=json.dumps(data),
            )

            pprint(response.status_code)

            if response.status_code != 200:
                raise GitcdGithubApiException(
                    "Could not fetch open pull requests," +
                    " please have a look manually."
                )
            pprint(response.json())