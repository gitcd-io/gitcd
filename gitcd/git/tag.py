from gitcd.git import Git

class Tag(Git):

    name = 'v'

    def __init__(self, name: str):
        self.name = name

    def getName(self) -> str:
        return self.name

    def delete(self) -> bool:
        output = self.verboseCli.execute("git tag -d %s" % (self.name))
        if output is False:
            return False
        return True
