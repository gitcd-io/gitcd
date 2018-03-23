from gitcd.git.server import GitServer
from gitcd.git.branch import Branch

from gitcd.exceptions import GitcdGithubApiException

import requests
from urllib.parse import urlencode

from pprint import pprint


class Gitlab(GitServer):

    tokenSpace = 'gitlab'
    baseUrl = 'https://gitlab.com/api/v4'

    def open(
        self,
        title: str,
        body: str,
        fromBranch: Branch,
        toBranch: Branch
    ) -> bool:
        token = self.configPersonal.getToken(self.tokenSpace)
        if token is not None:

            projectId = '%s%s%s' % (
                self.remote.getUsername(),
                '%2F',
                self.remote.getRepositoryName()
            )
            url = '%s/projects/%s/merge_requests' % (
                self.baseUrl,
                projectId
            )

            data = {
                'source_branch': fromBranch.getName(),
                'target_branch': toBranch.getName(),
                'title': title,
                'description': body
            }
            headers = {'Private-Token': token}
            response = requests.post(
                url,
                headers=headers,
                json=data
            )

            if response.status_code == 401:
                raise GitcdGithubApiException(
                    "Authentication failed, create a new app password."
                )

            if response.status_code == 409:
                raise GitcdGithubApiException(
                    "This pull-requests already exists."
                )

            # anything else but success
            if response.status_code != 201:
                raise GitcdGithubApiException(
                    "Open a pull request on gitlab failed."
                )

            try:
                jsonResponse = response.json()
                defaultBrowser = self.getDefaultBrowserCommand()
                self.cli.execute("%s %s" % (
                    defaultBrowser,
                    response.json()['web_url']
                ))
            except ValueError:
                raise GitcdGithubApiException(
                    "Open a pull request on gitlab failed."
                )
        else:
            defaultBrowser = self.getDefaultBrowserCommand()
            self.cli.execute("%s %s" % (
                defaultBrowser,
                "%s/%s/%s/merge_requests/new?%s=%s" % (
                    "https://gitlab.com",
                    self.remote.getUsername(),
                    self.remote.getRepositoryName(),
                    'merge_request%5Bsource_branch%5D',
                    fromBranch.getName()
                )
            ))
        return True

    def status(self, branch: Branch):
        master = Branch(self.config.getMaster())
        token = self.configPersonal.getToken(self.tokenSpace)
        if token is not None:

            data = {
                'state': 'biber',
                'source_branch': branch.getName(),
                'target_branch': master.getName()
            }

            projectId = '%s%s%s' % (
                self.remote.getUsername(),
                '%2F',
                self.remote.getRepositoryName()
            )
            baseUrl = "%s/projects/%s/merge_requests" % (
                self.baseUrl,
                projectId
            )
            url = "%s?state=opened" % (
                baseUrl
            )
            headers = {'Private-Token': token}
            response = requests.get(
                url,
                headers=headers,
                json=data
            )

            if response.status_code != 200:
                raise GitcdGithubApiException(
                    "Could not fetch open pull requests," +
                    " please have a look manually."
                )

            returnValue = {}
            responseJson = response.json()

            if len(responseJson) > 0:
                returnValue['state'] = 'REVIEW REQUIRED'
                reviewers = self.isReviewedBy(
                    "%s/%s/closes_issues" % (
                        baseUrl,
                        responseJson[0]['iid']
                    )
                )

                if len(reviewers) == 0:
                    reviewers = self.getLgtmComments(
                        "%s/%s/notes" % (
                            baseUrl,
                            responseJson[0]['iid']
                        )
                    )

                if len(reviewers) > 0:
                    returnValue['state'] = 'APPROVED'
                    for reviewer in reviewers:
                        reviewer = reviewers[reviewer]
                        if reviewer['state'] is not 'APPROVED':
                            returnValue['state'] = reviewer['state']

                returnValue['master'] = master.getName()
                returnValue['feature'] = branch.getName()
                returnValue['reviews'] = reviewers
                returnValue['url'] = responseJson[0]['web_url']
                returnValue['number'] = responseJson[0]['iid']

            return returnValue

    def isReviewedBy(self, activityUrl: str) -> dict:
        # not quite sure yet, need a different account to approve
        # a pull request
        return {}

        if token is not None:
            headers = {'Private-Token': token}
            response = requests.get(
                activityUrl,
                headers = headers
            )
            if response.status_code != 200:
                raise GitcdGithubApiException(
                    "Fetch PR activity for gitlab failed."
                )

            responseJson = response.json()
            reviewers = {}
            if ('values' in responseJson):
                for value in responseJson['values']:
                    if 'approval' in value:
                        reviewer = {}
                        reviewer['comments'] = []
                        approval = value['approval']
                        comment = {}
                        comment['date'] = approval['date']
                        comment['body'] = 'approved'
                        comment['state'] = 'APPROVED'
                        reviewer['state'] = 'APPROVED'
                        reviewer['comments'].append(comment)

                        reviewers[approval['user']['username']] = reviewer

        return reviewers

    def getLgtmComments(self, commentsUrl):
        token = self.configPersonal.getToken(self.tokenSpace)
        reviewers = {}
        if token is not None:
            headers = {'Private-Token': token}
            response = requests.get(
                commentsUrl,
                headers=headers
            )
            if response.status_code != 200:
                raise GitcdGithubApiException(
                    "Fetch PR comments for bitbucket failed."
                )

            comments = response.json()
            if len(comments) > 0:
                for comment in comments:
                    if (
                        'body' in comment and
                        'lgtm' in comment['body'].lower()
                    ):
                        if comment['author']['username'] in reviewers:
                            reviewer = reviewers[comment['author']['username']]
                        else:
                            reviewer = {}
                            reviewer['comments'] = []

                        reviewer['state'] = 'APPROVED'
                        reviewerComment = {}
                        reviewerComment['state'] = 'APPROVED'
                        reviewerComment['body'] = comment['body']
                        reviewer['comments'].append(reviewerComment)
                        reviewers[comment['author']['username']] = reviewer

        return reviewers
