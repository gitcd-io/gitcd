from gitcd.interface.cli.abstract import BaseCommand

from gitcd.git.branch import Branch


class Review(BaseCommand):

    def run(self, branch: Branch):
        self.interface.header('git-cd review')
        # @todo
