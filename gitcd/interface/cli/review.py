from gitcd.interface.cli.abstract import BaseCommand


class Review(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd review')
