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

            url = "%s/projects/%s/merge_requests?state=opened" % (
                self.baseUrl,
                projectId
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
            pprint(responseJson)

            if len(responseJson) > 1:
                #https://gitlab.example.com/api/v4/projects/76/merge_requests/1/closes_issues

            return returnValue
        #     if len(result) == 1:
        #         reviewers = self.isReviewedBy(
        #             '%s/%s' % (result[0]['url'], 'reviews')
        #         )

        #         returnValue['state'] = 'REVIEW REQUIRED'

        #         if len(reviewers) == 0:
        #             reviewers = self.getLgtmComments(result[0]['comments_url'])

        #         if len(reviewers) > 0:
        #             returnValue['state'] = 'APPROVED'
        #             for reviewer in reviewers:
        #                 reviewer = reviewers[reviewer]
        #                 if reviewer['state'] is not 'APPROVED':
        #                     returnValue['state'] = reviewer['state']

        #         returnValue['master'] = master.getName()
        #         returnValue['feature'] = branch.getName()
        #         returnValue['reviews'] = reviewers
        #         returnValue['url'] = result[0]['html_url']
        #         returnValue['number'] = result[0]['number']

        #     return returnValue







        #     if 'values' in responseJson and len(responseJson['values']) > 0:
        #         for pr in responseJson['values']:
        #             if (
        #                 'source' in pr and
        #                 'branch' in pr['source'] and
        #                 'name' in pr['source']['branch'] and
        #                 pr['source']['branch']['name'] == branch.getName()
        #             ):
        #                 currentPr = pr
        #                 reviewers = self.isReviewedBy(
        #                     currentPr['links']['activity']['href']
        #                 )

        #                 if len(reviewers) == 0:
        #                     reviewers = self.getLgtmComments(
        #                         currentPr['links']['comments']['href']
        #                     )

        #                 returnValue['state'] = 'REVIEW REQUIRED'

        #                 if len(reviewers) > 0:
        #                     returnValue['state'] = 'APPROVED'
        #                     for reviewer in reviewers:
        #                         reviewer = reviewers[reviewer]
        #                         if reviewer['state'] is not 'APPROVED':
        #                             returnValue['state'] = reviewer['state']

        #                 returnValue['master'] = master.getName()
        #                 returnValue['feature'] = branch.getName()
        #                 returnValue['reviews'] = reviewers
        #                 returnValue['url'] = currentPr['links']['html']['href']
        #                 returnValue['number'] = currentPr['id']

        # return returnValue

    def isReviewedBy(self, activityUrl: str) -> dict:
        # not quite sure yet, need a different account to approve
        # a pull request
        return {}

        token = self.getToken()
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
