from gitcd.Git.Command import Command
import time
from gitcd.Exceptions import GitcdNoDevelopmentBranchDefinedException

class Feature(Command):

  def getSubcommands(self):
    return [
      'start',
      'test',
      'review',
      'finish'
    ]

  def start(self, branch: str):
    self.interface.ok("gitcd feature start")

    origin = self.getOrigin()

    # ask for branch if nothing passed
    if branch == "*":
      branch = self.interface.askFor("Name for your new feature-branch? (without %s prefix)" % self.config.getFeature())

    featureBranch = "%s%s" % (self.config.getFeature(), branch)


    self.cli.execute("git checkout %s" % (self.config.getMaster()))
    self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))
    self.cli.execute("git checkout -b %s" % (featureBranch))
    self.cli.execute("git push %s %s" % (origin, branch))

  def test(self, branch: str):
    try:
      self.interface.ok("gitcd feature test")

      origin = self.getOrigin()
      developmentBranch = self.getDevelopmentBranch()

      featureBranch = self.getFeatureBranch(branch)

      self.cli.execute("git checkout %s" % (developmentBranch))
      self.cli.execute("git pull %s %s" % (origin, developmentBranch))
      self.cli.execute("git merge %s" % (featureBranch))
      self.cli.execute("git push %s %s" % (origin, developmentBranch))
    except GitcdNoDevelopmentBranchDefinedException as e:
      self.interface.writeOut("gitcd error: %s" % (format(e)))

  def review(self, branch: str):
    self.interface.ok("open a pull request on github")

    featureBranch = self.getFeatureBranch(branch)
    master = self.config.getMaster()
    repo = self.cli.execute("git remote show origin -n | grep h.URL | sed 's/.*://;s/.git$//'")
    token = self.config.getToken()

    if token != None:
      title = self.interface.askFor("Pull-Request title?")
      body = self.interface.askFor("Pull-Request body?")
      username = self.cli.execute("git config -l | grep credential | cut -d\"=\" -f 2")
      self.cli.execute("curl -s -u %s:%s -H \"Content-Type: application/json\" -X POST -d '{\"title\": \"%s\",\"body\": \"%s\",\"head\": \"%s\",\"base\": \"%s\"}' https://api.github.com/repos/%s/pulls" % (username, token, title, body, featureBranch, master, repo) )
    else: 
      self.interface.writeOut("open https://github.com/%s/compare/%s...%s" % (repo, master, featureBranch))
      self.cli.execute("open https://github.com/%s/compare/%s...%s" % (repo, master, featureBranch))

  def finish(self, branch: str):
    self.interface.ok("gitcd feature finish")

    origin = self.getOrigin()

    featureBranch = self.getFeatureBranch(branch)

    self.cli.execute("git checkout %s" % (self.config.getMaster()))
    self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))
    self.cli.execute("git merge %s" % (featureBranch))
    self.cli.execute("git push %s %s" % (origin, self.config.getMaster()))

    # push new tag
    if self.config.getVersionType() == 'manual':
      tagNumber = self.interface.askFor("Whats the current tag number you want to deliver?")
    else:
      tagNumber = time.strftime(self.config.getVersionScheme())

    tagMessage = self.interface.askFor("What message your new tag should have?")
    # escape double quotes for shell command
    tagMessage = tagMessage.replace('"', '\\"')
    self.cli.execute('git tag -a -m "%s" %s%s' % (tagMessage, self.config.getTag(), tagNumber))
    self.cli.execute("git push %s %s%s" % (origin, self.config.getTag(), tagNumber))

    deleteFeatureBranch = self.interface.askFor("Delete your feature branch?",
      ["yes", "no"],
      "yes"
    )

    if deleteFeatureBranch == "yes":
      # delete feature branch locally and remote
      self.cli.execute("git branch -D %s" % (featureBranch))
      self.cli.execute("git push %s :%s" % (origin, featureBranch))
