from gitcd.interface.cli.abstract import BaseCommand


class Test(BaseCommand):

    def run(self, branch: str):
        self.interface.header('git-cd test')
