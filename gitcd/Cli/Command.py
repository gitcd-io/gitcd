import subprocess
import string

class Command(object):

  def execute(self, command: str):
    cliArgs = self.parseCliArgs(command)

    process = subprocess.Popen(cliArgs, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    if process.returncode != 0:
      return False

    return output.decode("utf-8").strip()

  def parseCliArgs(self, command: str):
    rawArgs = command.split(" ")

    parsedArgs = []
    tmpString = False
    isSingle = False
    isDouble = False
    for arg in rawArgs:
      # handle  strings in single quotes
      if arg.startswith("'") and isSingle == False and isDouble == False:
        isSingle = True
        tmpString = arg

      elif arg.endswith("'") && isSingle == True:
        arg = "%s %s" % (tmpString, arg)
        parsedArgs.append(arg)
        isSingle = False
        tmpString = False

      # handle strings in double quotes
      elif arg.startswith('"') and isDouble == False and isSingle == False:
        isDouble = True
        tmpString = arg

      elif arg.endswith('"') && isDouble == True:
        arg = "%s %s" % (tmpString, arg)
        parsedArgs.append(arg)
        isDouble = False
        tmpString = False

      # extend current string
      elif tmpString != False:
        tmpString = "%s %s" % (tmpString, arg)

      else:
        parsedArgs.append(arg)

    return parsedArgs