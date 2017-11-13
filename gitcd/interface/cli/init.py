from gitcd.interface.cli.abstract import Abstract
import os


class Init(Abstract):

    def run(self, branch: str):
        self.cli.header('git-cd init')
