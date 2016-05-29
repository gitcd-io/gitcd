import subprocess
import string


from pprint import pprint


class Command(object):

  def execute(self, command):
    cliArgs = command.split(" ")

    process = subprocess.Popen(cliArgs, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    if process.returncode != 0:
      return False

    return output.decode("utf-8")
    #subprocess.call(command, shell = True)

  def executeRaw(self, command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().strip()

