from gitcd.git.repository import Repository


class Base(object):

    repository = None

    def __init__(self, repository: Repository):
        self.repository = repository
