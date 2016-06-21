import subprocess
import string
from gitcd.Cli.Interface import Interface
from gitcd.Exceptions import GitcdCliExecutionException

class Command(object):

  raiseException = False
  verbose = False
  interface = Interface()

  def setRaiseException(self, raiseException):
    self.raiseException = raiseException

  def setVerbose(self, verbose):
    self.verbose = verbose

  def getVerbose(self):
    return self.verbose

  def setRaiseException(self, raiseException):
    self.raiseException = raiseException

  def getRaiseException(self):
    return self.raiseException

  def execute(self, command):
    if self.verbose == True:
      self.interface.warning("Executing: %s" % command)

    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    if process.returncode != 0:
      if self.raiseException == True:
        raise GitcdCliExecutionException(err)
      return False

    return output.decode("utf-8").strip()
