from gitcd.config import Gitcd as GitcdConfig

from gitcd.git.repository import Repository


class Base(object):

    repository = None
    config = GitcdConfig()

    def __init__(self, repository: Repository):
        self.repository = repository
