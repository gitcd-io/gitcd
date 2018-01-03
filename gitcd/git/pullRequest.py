from gitcd.git import Git

from gitcd.git.branch import Branch

from gitcd.exceptions import GitcdGithubApiException
from gitcd.exceptions import GitcdGithubApiException

import json
import requests
from sys import platform


class RepositoryProvider(Git):

    def setRemote(self, remote) -> bool:
        self.remote = remote
        return True

    def openBrowser(self, url: str) -> bool:
        defaultBrowser = self.getDefaultBrowserCommand()
        self.cli.execute("%s %s" % (
            defaultBrowser,
            url
        ))
        return True

    def getDefaultBrowserCommand(self):
        if platform == "linux" or platform == "linux2":
            return "sensible-browser"
        elif platform == "darwin":
            return "open"
        elif platform == "win32":
            raise Exception("You have to be fucking kidding me")


class Github(RepositoryProvider):

    def open(self, title: str, body: str, fromBranch: Branch, toBranch: Branch) -> bool:
        token = self.configPersonal.getToken()
        url = "https://api.github.com/repos/%s/%s/pulls" % (self.remote.getUsername(), self.remote.getRepositoryName())

        # check if the token is a string - does not necessarily mean its valid
        if isinstance(token, str):
            data = {
                "title": title,
                "body": body,
                "head": fromBranch.getName(),
                "base": toBranch.getName()
            }

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
            self.cli.execute("%s %s" % (
                defaultBrowser,
                "https://github.com/%s/%s/compare/%s...%s" % (
                    username,
                    repo,
                    master,
                    featureBranch
                )
            ))
        return True

    def review(self):
        pass


class Bitbucket(RepositoryProvider):

    def open(self):
        pass

    def review(self):
        pass