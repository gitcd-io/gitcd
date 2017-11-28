from gitcd.interface.cli.abstract import BaseCommand


class Finish(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd finish')
