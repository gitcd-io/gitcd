from gitcd.interface.cli.abstract import BaseCommand


class Finish(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd finish')
