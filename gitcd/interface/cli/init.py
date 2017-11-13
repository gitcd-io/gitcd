from gitcd.interface.cli.abstract import BaseCommand
import os


class Init(BaseCommand):

    def run(self, branch: str):
        self.cli.header('git-cd init')
