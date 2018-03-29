from gitcd.git import Git
from sys import platform


class GitServer(Git):

    tokenSpace = None

    def getTokenSpace(self) -> str:
        return self.tokenSpace

    def setRemote(self, remote) -> bool:
        self.remote = remote
        return True

    def openBrowser(self, url: str) -> bool:
        defaultBrowser = self.getDefaultBrowserCommand()
        self.cli.execute("%s %s" % (
            defaultBrowser,
            url
        ))
        return True

    def getDefaultBrowserCommand(self):
        if platform == "linux" or platform == "linux2":
            return "sensible-browser"
        elif platform == "darwin":
            return "open"
        elif platform == "win32":
            raise Exception("You have to be fucking kidding me")

    def open(self):
        raise Exception('Not implemented')

    def status(self):
        raise Exception('Not implemented')
