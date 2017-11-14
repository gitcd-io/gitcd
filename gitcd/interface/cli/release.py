from gitcd.interface.cli.abstract import BaseCommand


class Release(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd release')
