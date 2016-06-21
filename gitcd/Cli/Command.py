import subprocess
import string
from gitcd.Cli.Interface import Interface
from gitcd.Exceptions import GitcdCliExecutionException

class Command(object):

  raiseException = False
  interface = Interface()

  def setRaiseException(self, raiseException):
    self.raiseException = raiseException

  def execute(self, command):
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    if process.returncode != 0:
      if self.raiseException == True:
        raise GitcdCliExecutionException(err.decode("utf-8").strip())
      return False

    return output.decode("utf-8").strip()
