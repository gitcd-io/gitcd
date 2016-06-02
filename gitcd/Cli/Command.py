import subprocess
import string

from pprint import pprint

class Command(object):

  def execute(self, command: str):
    #cliArgs = self.parseCliArgs(command)

    #pprint(cliArgs)

    process = subprocess.Popen(cliArgs, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    if process.returncode != 0:
      return False

    return output.decode("utf-8").strip()
