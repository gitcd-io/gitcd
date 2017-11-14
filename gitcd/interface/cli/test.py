from gitcd.interface.cli.abstract import BaseCommand


class Test(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd test')
