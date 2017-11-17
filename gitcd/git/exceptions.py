from gitcd.exceptions import GitcdException


class NoRepositoryException(GitcdException):
    pass


class RemoteNotFoundException(GitcdException):
    pass


class BranchNotFoundException(GitcdException):
    pass


class TagNotFoundException(GitcdException):
    pass
