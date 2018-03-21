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

            # <Response [409]>
            # {'message': ['Cannot Create: This merge request already exists: '
            # '["gitlab-integration"]']}

            # <Response [201]>
            # {'approvals_before_merge': None,
            #  'assignee': None,
            #  'author': {'avatar_url': 'https://secure.gravatar.com/avatar/22633d974a18183781ded24ef5e43374?s=80&d=identicon',
            #             'id': 2113833,
            #             'name': 'Claudio Walser',
            #             'state': 'active',
            #             'username': 'claudio-walser',
            #             'web_url': 'https://gitlab.com/claudio-walser'},
            #  'changes_count': '6',
            #  'closed_at': None,
            #  'closed_by': None,
            #  'created_at': '2018-03-15T17:39:44.316Z',
            #  'description': 'hoi',
            #  'discussion_locked': None,
            #  'downvotes': 0,
            #  'first_deployed_to_production_at': None,
            #  'force_remove_source_branch': None,
            #  'id': 8421843,
            #  'iid': 3,
            #  'labels': [],
            #  'latest_build_finished_at': None,
            #  'latest_build_started_at': None,
            #  'merge_commit_sha': None,
            #  'merge_status': 'can_be_merged',
            #  'merge_when_pipeline_succeeds': False,
            #  'merged_at': None,
            #  'merged_by': None,
            #  'milestone': None,
            #  'pipeline': None,
            #  'project_id': 5760416,
            #  'sha': '11305bb6acfad8d9e6f9f99ecf1cf483c3f2e30b',
            #  'should_remove_source_branch': None,
            #  'source_branch': 'gitlab-integration',
            #  'source_project_id': 5760416,
            #  'squash': False,
            #  'state': 'opened',
            #  'subscribed': True,
            #  'target_branch': 'master',
            #  'target_project_id': 5760416,
            #  'time_stats': {'human_time_estimate': None,
            #                 'human_total_time_spent': None,
            #                 'time_estimate': 0,
            #                 'total_time_spent': 0},
            #  'title': 'gitlab-integration',
            #  'updated_at': '2018-03-15T17:39:44.316Z',
            #  'upvotes': 0,
            #  'user_notes_count': 0,
            #  'web_url': 'https://gitlab.com/claudio-walser/gitcd/merge_requests/3',
            #  'work_in_progress': False}

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
