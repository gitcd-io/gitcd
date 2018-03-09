from gitcd.git.server import GitServer
from gitcd.git.branch import Branch

from gitcd.exceptions import GitcdGithubApiException

import json
import requests
from pprint import pprint


class Bitbucket(GitServer):

    tokenSpace = 'bitbucket'
    baseUrl = 'https://api.bitbucket.org/2.0'

    def open(
        self,
        title: str,
        body: str,
        fromBranch: Branch,
        toBranch: Branch
    ) -> bool:

        # https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Busername%7D/%7Brepo_slug%7D/pullrequests#post
        # https://community.atlassian.com/t5/Bitbucket-questions/Creating-a-pull-request-via-API/qaq-p/123913
        # https://blog.bitbucket.org/2013/11/12/api-2-0-new-function-and-enhanced-usability
        # https://github.com/cdancy/bitbucket-rest
        # https://bitbucket.org/site/master/issues/8195/rest-api-for-creating-pull-requests
        # https://api.bitbucket.org/2.0/repositories/{user}/{slug}/pullrequests/
        token = self.configPersonal.getToken('bitbucket')

        if isinstance(token, str) and ':' in token:

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

            auth = token.split(':')
            response = requests.post(
                url,
                json=data,
                auth=(auth[0], auth[1])
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
                        "Open a pull request on bitbucket failed with message: %s" % (
                            message
                        )
                    )
                except ValueError:
                    raise GitcdGithubApiException(
                        "Open a pull request on bitbucket failed for an unknown reason."
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
                "https://bitbucket.org/%s/%s/pull-requests/new?source=%s&event_source=gitcd" % (
                    self.remote.getUsername(),
                    self.remote.getRepositoryName(),
                    fromBranch.getName()
                )
            ))
        return True

    def status(self, branch: Branch):
        token = self.configPersonal.getToken('bitbucket')
        master = Branch(self.config.getMaster())
        if isinstance(token, str) and ':' in token:
            url = "%s/repositories/%s/%s/pullrequests" % (
                self.baseUrl,
                self.remote.getUsername(),
                self.remote.getRepositoryName()
            )

            auth = token.split(':')

            response = requests.get(
                url,
                auth=(auth[0], auth[1])
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
                    if 'source' in pr and 'branch' in pr['source'] and 'name' in pr['source']['branch'] and pr['source']['branch']['name'] == branch.getName():
                        currentPr = pr
                        returnValue['state'] = 'REVIEW REQUIRED'
                        returnValue['master'] = master.getName()
                        returnValue['feature'] = branch.getName()
                        #returnValue['reviews'] = reviewers
                        returnValue['reviews'] = {}
                        returnValue['url'] = currentPr['links']['html']['href']
                        returnValue['number'] = currentPr['id']
            

        return returnValue