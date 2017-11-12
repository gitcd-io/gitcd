import subprocess
import string
from gitcd.Cli.Interface import Interface
from gitcd.Exceptions import GitcdCliExecutionException


class Command(object):

    raiseException = False
    verbose = False
    interface = Interface()

    def setVerbose(self, verbose: bool):
        self.verbose = verbose

    def getVerbose(self):
        return self.verbose

    def setRaiseException(self, raiseException: bool):
        self.raiseException = raiseException

    def getRaiseException(self):
        return self.raiseException

    def execute(self, command: str, codeOk: int = 0):
        if self.verbose is True:
            self.interface.warning("Executing: %s" % command)

        process = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, err = process.communicate()
        if process.returncode != codeOk:
            if self.raiseException is True:
                raise GitcdCliExecutionException(err.decode("utf-8").strip())
            return False

        output = output.decode("utf-8").strip()
        if self.verbose is True:
            self.interface.writeOut(output)

        return output
