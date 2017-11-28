from gitcd.interface.cli.abstract import BaseCommand


class Start(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd start')
