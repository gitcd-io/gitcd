from gitcd.git.server import GitServer
from gitcd.git.branch import Branch

from gitcd.exceptions import GitcdGithubApiException

import requests


class Gitlab(GitServer):

    tokenSpace = 'gitlab'
    baseUrl = 'https://api.bitbucket.org/2.0'

    def getAuth(self):
        token = self.configPersonal.getToken(self.tokenSpace)
        if isinstance(token, str) and ':' in token:
            auth = token.split(':')
            return (auth[0], auth[1])
        return None

    def open(
        self,
        title: str,
        body: str,
        fromBranch: Branch,
        toBranch: Branch
    ) -> bool:
        raise Exception('needs to be implemented')



        auth = self.getAuth()
        if auth is not None:
            url = "%s/repositories/%s/%s/pullrequests" % (
                self.baseUrl,
                self.remote.getUsername(),
                self.remote.getRepositoryName()
            )

            data = {
                "destination": {
                    "branch": {
                        "name": toBranch.getName()
                    }
                },
                "source": {
                    "branch": {
                      "name": fromBranch.getName()
                    }
                },
                "title": title,
                "description": body
            }

            response = requests.post(
                url,
                json=data,
                auth=auth
            )

            if response.status_code == 401:
                raise GitcdGithubApiException(
                    "Authentication failed, create a new app password."
                )

            if response.status_code != 201:
                try:
                    jsonResponse = response.json()
                    message = jsonResponse['error']['message']
                    raise GitcdGithubApiException(
                        "Open a pull request on bitbucket" +
                        " failed with message: %s" % (
                            message
                        )
                    )
                except ValueError:
                    raise GitcdGithubApiException(
                        "Open a pull request on bitbucket failed."
                    )

            defaultBrowser = self.getDefaultBrowserCommand()
            self.cli.execute("%s %s" % (
                defaultBrowser,
                response.json()["links"]['html']['href']
            ))
        else:
            defaultBrowser = self.getDefaultBrowserCommand()
            self.cli.execute("%s %s" % (
                defaultBrowser,
                "%s/%s/%s/pull-requests/new?source=%s&event_source=gitcd" % (
                    "https://bitbucket.org",
                    self.remote.getUsername(),
                    self.remote.getRepositoryName(),
                    fromBranch.getName()
                )
            ))
        return True

    def status(self, branch: Branch):
        raise Exception('needs to be implemented')

        master = Branch(self.config.getMaster())
        auth = self.getAuth()
        if auth is not None:
            url = "%s/repositories/%s/%s/pullrequests" % (
                self.baseUrl,
                self.remote.getUsername(),
                self.remote.getRepositoryName()
            )

            response = requests.get(
                url,
                auth=auth
            )

            if response.status_code != 200:
                raise GitcdGithubApiException(
                    "Could not fetch open pull requests," +
                    " please have a look manually."
                )

            returnValue = {}
            responseJson = response.json()
            if 'values' in responseJson and len(responseJson['values']) > 0:
                for pr in responseJson['values']:
                    if (
                        'source' in pr and
                        'branch' in pr['source'] and
                        'name' in pr['source']['branch'] and
                        pr['source']['branch']['name'] == branch.getName()
                    ):
                        currentPr = pr
                        reviewers = self.isReviewedBy(
                            currentPr['links']['activity']['href']
                        )

                        if len(reviewers) == 0:
                            reviewers = self.getLgtmComments(
                                currentPr['links']['comments']['href']
                            )

                        returnValue['state'] = 'REVIEW REQUIRED'

                        if len(reviewers) > 0:
                            returnValue['state'] = 'APPROVED'
                            for reviewer in reviewers:
                                reviewer = reviewers[reviewer]
                                if reviewer['state'] is not 'APPROVED':
                                    returnValue['state'] = reviewer['state']

                        returnValue['master'] = master.getName()
                        returnValue['feature'] = branch.getName()
                        returnValue['reviews'] = reviewers
                        returnValue['url'] = currentPr['links']['html']['href']
                        returnValue['number'] = currentPr['id']

        return returnValue

    def isReviewedBy(self, activityUrl: str) -> dict:
        raise Exception('needs to be implemented')

        auth = self.getAuth()
        if auth is not None:
            response = requests.get(
                activityUrl,
                auth=auth
            )
            if response.status_code != 200:
                raise GitcdGithubApiException(
                    "Fetch PR activity for bitbucket failed."
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
        raise Exception('needs to be implemented')

        auth = self.getAuth()
        reviewers = {}
        if auth is not None:
            response = requests.get(
                commentsUrl,
                auth=auth
            )
            if response.status_code != 200:
                raise GitcdGithubApiException(
                    "Fetch PR comments for bitbucket failed."
                )

            comments = response.json()

            if 'values' in comments:
                for comment in comments['values']:
                    if (
                        'content' in comment and
                        'lgtm' in comment['content']['raw'].lower()
                    ):
                        if comment['user']['username'] in reviewers:
                            reviewer = reviewers[comment['user']['username']]
                        else:
                            reviewer = {}
                            reviewer['comments'] = []

                        reviewer['state'] = 'APPROVED'
                        reviewerComment = {}
                        reviewerComment['state'] = 'APPROVED'
                        reviewerComment['body'] = comment['content']['raw']
                        reviewer['comments'].append(reviewerComment)
                        reviewers[comment['user']['username']] = reviewer

        return reviewers
