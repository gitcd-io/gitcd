import subprocess
import string


from pprint import pprint


class Command(object):

  def execute(self, command: str):
    print(command)
    cliArgs = command.split(" ")
    subprocess.call(command, shell = True)
