from gitcd.git.repository import Repository


class Base(object):

    repository = Repository()
    config = None
    configPersonal = None

    def __init__(self):
        self.config = self.repository.getConfig()
        self.configPersonal = self.repository.getPersonalConfig()
