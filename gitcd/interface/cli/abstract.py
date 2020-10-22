import simpcli
import sys

from gitcd.git.repository import Repository
from gitcd.git.branch import Branch
from gitcd.git.tag import Tag
from gitcd.git.remote import Remote

from gitcd.config import Gitcd as GitcdConfig
from gitcd.config import GitcdPersonal as GitcdPersonalConfig

from gitcd.exceptions import GitcdNoFeatureBranchException


class BaseCommand(object):

    interface = simpcli.Interface()
    repository = None
    config = None
    configPersonal = GitcdPersonalConfig()
    updateRemote = False

    def __init__(self):
        self.instantiateRepository()
        self.instantiateConfig()
        if self.updateRemote is True:
            self.repository.update()

    def instantiateRepository(self) -> bool:
        self.repository = Repository()
        return True

    def instantiateConfig(self):
        self.config = GitcdConfig(self.repository.getRootDirectory())

    def run(self, branch: Branch):
        pass

    def getDefaultBranch(self) -> Branch:
        return self.repository.getCurrentBranch()

    def getRequestedBranch(self, branch: str) -> Branch:
        featureAsString = self.config.getString(self.config.getFeature())
        if (
            not branch.startswith(featureAsString) and
            branch != self.config.getMaster()
        ):
            branch = '%s%s' % (featureAsString, branch)
        return Branch(branch)

    def hasMultipleRemotes(self) -> bool:
        return len(self.repository.getRemotes()) > 1

    def getRemote(self, whatFor: str = "") -> str:
        remotes = self.repository.getRemotes()

        if len(remotes) == 1:
            remote = remotes[0]
        else:
            if len(remotes) == 0:
                default = False
                choice = False
            else:
                default = remotes[0].getName()
                choice = []
                for remoteObj in remotes:
                    choice.append(remoteObj.getName())

            if whatFor:
                whatFor = " {}".format(whatFor)

            msg = "Which remote you want to use{}?".format(whatFor)
            remoteAnswer = self.interface.askFor(
                msg,
                choice,
                default
            )
            for remoteObj in remotes:
                if remoteAnswer == remoteObj.getName():
                    remote = remoteObj

        return remote

    def checkTag(self, remote: Remote, tag: Tag) -> bool:
        if self.repository.hasUncommitedChanges():
            abort = self.interface.askFor(
                "You currently have uncomitted changes." +
                " Do you want me to abort and let you commit first?",
                ["yes", "no"],
                "yes"
            )

            if abort == "yes":
                sys.exit(1)

        return True

    def checkRepository(self) -> bool:
        # check if repo has uncommited changes
        if self.repository.hasUncommitedChanges():
            abort = self.interface.askFor(
                "You currently have uncomitted changes." +
                " Do you want me to abort and let you commit first?",
                ["yes", "no"],
                "yes"
            )

            if abort == "yes":
                sys.exit(1)

        return True

    def checkBranch(self, remote: Remote, branch: Branch) -> bool:
        # check if its a feature branch
        if not branch.isFeature():
            raise GitcdNoFeatureBranchException(
                "Your current branch is not a valid feature branch." +
                " Checkout a feature branch or pass one as param."
            )

        # check remote existence
        if not remote.hasBranch(branch):
            pushFeatureBranch = self.interface.askFor(
                "Your feature branch does not exist on remote." +
                " Do you want me to push it remote?", ["yes", "no"], "yes"
            )

            if pushFeatureBranch == "yes":
                remote.push(branch)

        # check behind origin
        if remote.isBehind(branch):

            pushFeatureBranch = self.interface.askFor(
                "Your feature branch is ahead the origin/branch." +
                " Do you want me to push the changes?",
                ["yes", "no"],
                "yes"
            )

            if pushFeatureBranch == "yes":
                remote.push(branch)

        return True

    def getTokenOrAskFor(self, tokenSpace: str) -> str:
        token = self.configPersonal.getToken(tokenSpace)
        if token is None:
            token = self.interface.askFor(
                "Your personal %s token?" % (tokenSpace),
                False,
                token
            )

            if (
                tokenSpace == 'bitbucket' and
                ':' not in token
            ):
                self.interface.warning(
                    'For bitbucket you need to pass a username' +
                    ' as well like <username:app_password>'
                )
                return self.getTokenOrAskFor(tokenSpace)

            self.configPersonal.setToken(tokenSpace, token)
            self.configPersonal.write()
        return token

    def mergeWithRetry(self, remote, sourceBranch, targetBranch):
        try:
            remote.merge(sourceBranch, targetBranch)
        except simpcli.CliException:
            tryAgain = self.interface.askFor(
                "An error occured during the merge.\
                Do you want to fix it and let me try it again?",
                ["yes", "no"], "yes"
            )

            if tryAgain == 'yes':
                self.mergeWithRetry(remote, sourceBranch, targetBranch)
