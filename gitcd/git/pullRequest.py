from gitcd.git import Git
from gitcd.git.branch import Branch

from gitcd.exceptions import GitcdGithubApiException

import json
import requests
from sys import platform

from pprint import pprint


class RepositoryProvider(Git):

    tokenSpace = None

    def getTokenSpace(self) -> str:
        return self.tokenSpace

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

    def open(self):
        raise Exception('Not implemented')

    def status(self):
        raise Exception('Not implemented')


class Github(RepositoryProvider):

    tokenSpace = 'github'

    def open(
        self,
        title: str,
        body: str,
        fromBranch: Branch,
        toBranch: Branch
    ) -> bool:
        token = self.configPersonal.getToken('github')
        url = "https://api.github.com/repos/%s/%s/pulls" % (
            self.remote.getUsername(),
            self.remote.getRepositoryName()
        )

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
                    self.remote.getUsername(),
                    self.remote.getRepositoryName(),
                    toBranch.getName(),
                    fromBranch.getName()
                )
            ))
        return True

    def status(self, branch: Branch):
        username = self.remote.getUsername()
        ref = "%s:refs/heads/%s" % (username, branch.getName())
        token = self.configPersonal.getToken('github')
        master = Branch(self.config.getMaster())
        # claudio-walser:refs/heads/implement-status
        if isinstance(token, str):
            url = "https://api.github.com/repos/%s/%s/pulls" % (
                username,
                self.remote.getRepositoryName()
            )

            data = {
                "state": 'open',
                "head": ref,
                "base": master.getName()
            }

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
            returnValue = {}
            if len(result) == 1:
                reviewers = self.isReviewedBy(
                    '%s/%s' % (result[0]['url'], 'reviews')
                )

                returnValue['state'] = 'REVIEW REQUIRED'

                if len(reviewers) == 0:
                    reviewers = self.getLgtmComments(result[0]['comments_url'])

                if len(reviewers) > 0:
                    returnValue['state'] = 'APPROVED'
                    for reviewer in reviewers:
                        reviewer = reviewers[reviewer]
                        if reviewer['state'] is not 'APPROVED':
                            returnValue['state'] = reviewer['state']

                returnValue['master'] = master.getName()
                returnValue['feature'] = branch.getName()
                returnValue['reviews'] = reviewers
                returnValue['url'] = result[0]['html_url']
                returnValue['number'] = result[0]['number']

            return returnValue

    def isReviewedBy(self, reviewUrl) -> dict:
        token = self.configPersonal.getToken('github')
        reviewers = {}
        if isinstance(token, str):
            if token is not None:
                headers = {'Authorization': 'token %s' % token}
                response = requests.get(
                    reviewUrl,
                    headers=headers
                )
                reviews = response.json()
                for review in reviews:
                    if review['user']['login'] in reviewers:
                        reviewer = reviewers[review['user']['login']]
                    else:
                        reviewer = {}
                        reviewer['comments'] = []

                    comment = {}
                    comment['date'] = review['submitted_at']
                    comment['body'] = review['body']
                    comment['state'] = review['state']
                    reviewer['state'] = review['state']
                    reviewer['comments'].append(comment)

                    reviewers[review['user']['login']] = reviewer

        return reviewers

    def getLgtmComments(self, commentsUrl):
        token = self.configPersonal.getToken('github')
        reviewers = {}
        if isinstance(token, str):
            if token is not None:
                headers = {'Authorization': 'token %s' % token}
                response = requests.get(
                    commentsUrl,
                    headers=headers
                )
                comments = response.json()
                for comment in comments:
                    if 'lgtm' in comment['body'].lower():

                        if comment['user']['login'] in reviewers:
                            reviewer = reviewers[comment['user']['login']]
                        else:
                            reviewer = {}

                        reviewer['state'] = 'APPROVED'
                        reviewer['comments'] = []
                        reviewerComment = {}
                        reviewerComment['state'] = 'APPROVED'
                        reviewerComment['body'] = comment['body']
                        reviewer['comments'].append(reviewerComment)
                        reviewers[comment['user']['login']] = reviewer

        return reviewers


class Bitbucket(RepositoryProvider):

    tokenSpace = 'bitbucket'

    def open(
        self,
        title: str,
        body: str,
        fromBranch: Branch,
        toBranch: Branch
    ) -> bool:

        # https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Busername%7D/%7Brepo_slug%7D/pullrequests#post
        # https://community.atlassian.com/t5/Bitbucket-questions/Creating-a-pull-request-via-API/qaq-p/123913
        # https://blog.bitbucket.org/2013/11/12/api-2-0-new-function-and-enhanced-usability/
        token = self.configPersonal.getToken('bitbucket')
        url = "%s/repositories/%s/%s/pullrequests" % (
            'https://api.bitbucket.org/2.0',
            self.remote.getUsername(),
            self.remote.getRepositoryName()
        )

        data = {
            "title": title,
            "description": body,
            "source": self.remote.getUrl(),
            "fromRef": {
                "id": "refs/heads/%s" % (fromBranch.getName()),
                "repository": {
                    "slug": self.remote.getRepositoryName(),
                    "name": None,
                    "project": {
                        "key": self.remote.getRepositoryName()
                    }
                }
            },
            "toRef": {
                "id": "refs/heads/%s" % (toBranch.getName()),
                "repository": {
                    "slug": self.remote.getRepositoryName(),
                    "name": None,
                    "project": {
                        "key": self.remote.getRepositoryName()
                    }
                }
            }
        }

        response = requests.post(
            url,
            #headers=headers,
            data=json.dumps(data),
        )
        pprint(url)
        pprint(response.json())
        pprint(json.dumps(data))
        pass

        # if response.status_code != 201:
        #     jsonResponse = response.json()
        #     message = jsonResponse['errors'][0]['message']
        #     raise GitcdGithubApiException(
        #         "Open a pull request failed with message: %s" % (
        #             message
        #         )
        #     )

        # defaultBrowser = self.getDefaultBrowserCommand()
        # self.cli.execute("%s %s" % (
        #     defaultBrowser,
        #     response.json()["html_url"]
        # ))

        # return True

    def status(self):
        pass
