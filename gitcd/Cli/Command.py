import subprocess
import string


from pprint import pprint


class Command(object):

  def execute(self, command: str):
    cliArgs = command.split(" ")

    pprint(cliArgs)
    #subprocess.Popen(cliArgs)
    subprocess.call(command, shell = True)


    print(command)