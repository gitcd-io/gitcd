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
        ref = "%s:refs/heads/%s" % (username, featureBranch)
        # claudio-walser:refs/heads/implement-status
        if isinstance(token, str):
            url = "https://api.github.com/repos/%s/%s/pulls" % (username, repo)

            data = {
                "state": 'open',
                "head": ref,
                "base": master
            }

            self.interface.warning("Fetch pull-request infos on %s" % (url))

            headers = {'Authorization': 'token %s' % token}
            response = requests.get(
                url,
                headers=headers,
                params=data
            )

            if response.status_code != 200:
                raise GitcdGithubApiException(
                    "Could not fetch open pull requests," +
                    " please have a look manually."
                )

            result = response.json()

            if len(result) == 1:
                reviewedBy = self.isReviewedBy(
                    result[0]['comments_url']
                )
                self.interface.ok("Pull Request Info")
                self.interface.info("Branches: %s...%s" % (
                    featureBranch,
                    master)
                )
                self.interface.info("Number:   %s" % (result[0]['number']))
                self.interface.info("Reviewd by: %s" % (reviewedBy))
                self.interface.info("URL: %s" % (result[0]['html_url']))

                # if not reviewed yet
                if reviewedBy is '':
                    reviewPullRequest = self.interface.askFor(
                        "Do you want to review this pull \
                        request in your Browser?", [
                            "yes",
                            "no"
                        ], "yes"
                    )

                    if reviewPullRequest == "yes":
                        # delete feature branch remote and locally
                        defaultBrowser = self.getDefaultBrowserCommand()
                        self.cli.execute("%s %s" % (
                            defaultBrowser,
                            "%s/files" % (result[0]['html_url'])
                        ))
            else:
                self.interface.error(
                    "No pull request exists for %s...%s" % (
                        featureBranch,
                        master
                    )
                )
                self.interface.info(
                    "Run git-cd review %s to create a pull request" % (
                        featureBranch
                    )
                )

    def isReviewedBy(self, commentsUrl):
        token = self.getTokenOrAskFor()
        pprint(commentsUrl)
        if token is not None:
            headers = {'Authorization': 'token %s' % token}
            response = requests.get(
                commentsUrl,
                headers=headers
            )
            pprint(response.json())

        return ''
