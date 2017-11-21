from gitcd.git.repository import Repository


class Base(object):

    repository = None
    config = None

    def __init__(self, repository: Repository):
        self.repository = repository
        self.config = self.repository.getConfig()
        self.configPersonal = self.repository.getPersonalConfig()
