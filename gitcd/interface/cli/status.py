from gitcd.interface.cli.abstract import BaseCommand


class Status(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd status')
