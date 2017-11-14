from gitcd.interface.cli.abstract import BaseCommand


class Start(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd start')
