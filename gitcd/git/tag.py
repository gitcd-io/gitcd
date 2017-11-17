from gitcd.git import Git

class Tag(Git):

    name = 'v'

    def __init__(self, name: str):
        self.name = name

    def getName(self) -> str:
        return self.name

    def delete(self) -> bool:
        print('delete tag %s' % self.getName())
        pass
