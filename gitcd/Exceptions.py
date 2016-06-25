class GitcdException(Exception):
  pass

class GitcdArgumentsException(Exception):
  pass

class GitcdFileNotFoundException(Exception):
  pass

class GitcdNoRepositoryException(Exception):
  pass

class GitcdNoFeatureBranchException(Exception):
  pass

class GitcdNoDevelopmentBranchDefinedException(Exception):
  pass

class GitcdCliExecutionException(Exception):
  pass