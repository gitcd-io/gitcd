from gitcd.git.server import GitServer
from gitcd.git.branch import Branch

from gitcd.exceptions import GitcdGithubApiException

import json
import requests


class Github(GitServer):

    tokenSpace = 'github'
    baseUrl = 'https://api.github.com'

    def open(
        self,
        title: str,
        body: str,
        fromBranch: Branch,
        toBranch: Branch,
        sourceRemote=None
    ) -> bool:
        token = self.configPersonal.getToken(self.tokenSpace)
        url = "%s/repos/%s/%s/pulls" % (
            self.baseUrl,
            self.remote.getUsername(),
            self.remote.getRepositoryName()
        )
        head = ''
        if sourceRemote is not None:
            # check sourceRemote is github as well
            if sourceRemote.isGithub() is not True:
                raise GitcdGithubApiException(
                    "Github is not able to get a pr from a different server"
                )
            head = '%s:' % (sourceRemote.getUsername())
        # check if the token is a string - does not necessarily mean its valid
        if isinstance(token, str):
            data = {
                "title": title,
                "body": body,
                "head": '%s%s' % (head, fromBranch.getName()),
                "base": toBranch.getName()
            }

            headers = {'Authorization': 'token %s' % token}
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(data),
            )

            if response.status_code == 401:
                raise GitcdGithubApiException(
                    "Authentication failed, create a new access token."
                )

            if response.status_code != 201:
                try:
                    jsonResponse = response.json()
                    from pprint import pprint
                    pprint(jsonResponse)
                    message = jsonResponse['message']
                    raise GitcdGithubApiException(
                        "Open a pull request failed with message: %s" % (
                            message
                        )
                    )
                except ValueError:
                    raise GitcdGithubApiException(
                        "Open a pull request on github failed."
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

    def status(self, branch: Branch, sourceRemote=None):
        username = self.remote.getUsername()
        if sourceRemote is not None:
            # check sourceRemote is github as well
            if sourceRemote.isGithub() is not True:
                raise GitcdGithubApiException(
                    "Github is not able to see a pr from a different server"
                )
            ref = '%s:%s' % (sourceRemote.getUsername(), branch.getName())
        else:
            ref = "%s:refs/heads/%s" % (username, branch.getName())

        token = self.configPersonal.getToken(self.tokenSpace)
        master = Branch(self.config.getMaster())
        if isinstance(token, str):
            url = "%s/repos/%s/%s/pulls" % (
                self.baseUrl,
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
                        if reviewer['state'] != 'APPROVED':
                            returnValue['state'] = reviewer['state']

                returnValue['master'] = master.getName()
                returnValue['feature'] = branch.getName()
                returnValue['reviews'] = reviewers
                returnValue['url'] = result[0]['html_url']
                returnValue['number'] = result[0]['number']

            return returnValue

    def isReviewedBy(self, reviewUrl) -> dict:
        token = self.configPersonal.getToken(self.tokenSpace)
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
        token = self.configPersonal.getToken(self.tokenSpace)
        reviewers = {}
        if isinstance(token, str):
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
                        reviewer['comments'] = []

                    reviewer['state'] = 'APPROVED'
                    reviewerComment = {}
                    reviewerComment['state'] = 'APPROVED'
                    reviewerComment['body'] = comment['body']
                    reviewer['comments'].append(reviewerComment)
                    reviewers[comment['user']['login']] = reviewer

        return reviewers
