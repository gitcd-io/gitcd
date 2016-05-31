import subprocess
import string

class Command(object):

  def execute(self, command):
    cliArgs = command.split(" ")

    process = subprocess.Popen(cliArgs, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    if process.returncode != 0:
      return False

    return output.decode("utf-8").strip()
