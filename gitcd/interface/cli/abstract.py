import simpcli

class BaseCommand(object):

    cli = simpcli.Interface()

    def run(self, branch: str):
        pass
