import os
from typing import List

from gitcd.git.repository import Repository

class NullRepository(Repository):

    def __init__(self):
        self.directory = ""

    def getCurrentBranch(self) -> None:
        return None
