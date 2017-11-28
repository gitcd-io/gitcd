from gitcd.interface.cli.abstract import BaseCommand


class Release(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd release')
