from gitcd.interface.cli.abstract import BaseCommand


class Compare(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd compare')
        # @todo
