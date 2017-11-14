from gitcd.interface.cli.abstract import BaseCommand


class Compare(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd compare')
