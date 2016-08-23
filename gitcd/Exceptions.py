class GitcdException(Exception):
    pass


class GitcdArgumentsException(GitcdException):
    pass


class GitcdFileNotFoundException(GitcdException):
    pass


class GitcdNoRepositoryException(GitcdException):
    pass


class GitcdNoFeatureBranchException(GitcdException):
    pass


class GitcdNoDevelopmentBranchDefinedException(GitcdException):
    pass


class GitcdCliExecutionException(GitcdException):
    pass


class GitcdGithubApiException(GitcdException):
    pass
