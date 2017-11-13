import simpcli

class Abstract(object):

    cli = simpcli.Interface()

    def run(self, branch: str):
        pass
