from gitcd.interface.cli.abstract import BaseCommand


class Status(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd status')
