from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.branch import Branch


class Status(BaseCommand):

    def run(self, branch: str):
        remote = self.getRemote()
        self.getTokenOrAskFor()
        master = Branch(self.config.getMaster())
        prInfo = remote.statusPullRequest(branch)
        if len(prInfo) is 0:
            self.interface.writeOut(
                "No pull request exists for %s...%s\n" % (
                    branch.getName(),
                    master.getName()
                )
            )

            self.interface.writeOut('Run')
            self.interface.warning(
                "git-cd review %s" % (
                    branch.getName()
                )
            )
            self.interface.writeOut('to create a pull request')
        else:
            self.interface.writeOut("Branches: %s...%s" % (
                branch.getName(),
                master.getName())
            )
            if prInfo['state'] == 'APPROVED':
                state = '%s%s%s' % (
                    self.interface.OK,
                    prInfo['state'],
                    self.interface.ENDC
                )
            else:
                state = '%s%s%s' % (
                    self.interface.ERROR,
                    prInfo['state'],
                    self.interface.ENDC
                )
            self.interface.writeOut('State: %s' % (state))
            self.interface.writeOut("Number:   %s" % (prInfo['number']))
            self.interface.writeOut("Reviews:")
            for user in prInfo['reviews']:
                review = prInfo['reviews'][user]
                self.interface.writeOut('    - %s' % (user))
                for comment in review['comments']:
                    if comment['state'] == 'APPROVED':
                        state = '%s%s%s' % (
                            self.interface.OK,
                            comment['state'],
                            self.interface.ENDC
                        )
                    else:
                        state = '%s%s%s' % (
                            self.interface.ERROR,
                            comment['state'],
                            self.interface.ENDC
                        )
                    self.interface.writeOut('        %s: %s' % (
                        state,
                        comment['body']
                    ))

            self.interface.writeOut("URL: %s" % (prInfo['url']))
