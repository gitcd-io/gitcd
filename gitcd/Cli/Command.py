import subprocess
import string

class Command(object):

  def execute(self, command: str):
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    if process.returncode != 0:
      return False

    return output.decode("utf-8").strip()
