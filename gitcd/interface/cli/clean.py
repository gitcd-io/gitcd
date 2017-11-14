from gitcd.interface.cli.abstract import BaseCommand


class Clean(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd clean')
