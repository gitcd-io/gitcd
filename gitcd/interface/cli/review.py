from gitcd.interface.cli.abstract import BaseCommand


class Review(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd review')
