from gitcd.Git.Abstract import Abstract
import time

class Feature(Abstract):

  def start(self, branch):

    origin = self.getOrigin()

    if branch == None:
      branch = self.interface.askFor("Name your new Branch?")

    branch = self.config.getFeature().branch


    self.cli.execute("git checkout %s" % (self.config.getMaster()))
    self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))
    self.cli.execute("git checkout -b %s" % (branch))
    self.cli.execute("git push %s %s%s" % (origin, self.config.getFeature(), branch))


    self.interface.ok("gitcd feature start: ".branch)

  def test(self, branch):

    origin = self.getOrigin()
    developmentBranch = self.getDevelopmentBranch()

    if branch == None:
      branch = self.cli.executeRaw("git rev-parse --abbrev-ref HEAD")
    else: 
      branch = self.config.getFeature().branch
      

    # todo: need to handle this as prefix and read all possible branches
    # ask user if more than one possibillities
    self.cli.execute("git checkout %s" % (developmentBranch))
    self.cli.execute("git pull %s %s" % (origin, developmentBranch))
    self.cli.execute("git merge %s" % (branch))
    self.cli.execute("git push %s %s" % (origin, developmentBranch))

    self.interface.ok("gitcd feature test: ".branch)

  def review(self, branch):

    if branch == None:
      branch = self.cli.executeRaw("git rev-parse --abbrev-ref HEAD")
    else: 
      branch = self.config.getFeature().branch

    master = self.config.getMaster()

    repo = self.cli.executeRaw("git remote show origin -n | grep h.URL | sed 's/.*://;s/.git$//'")
    
    token = self.config.getToken()

    if token != None:
      title = self.interface.askFor("Pullrequtest Title?")
      body = self.interface.askFor("Pullrequtest Body?")
      username = self.cli.executeRaw("git config -l | grep credential | cut -d\"=\" -f 2")
      self.cli.executeRaw("curl -s -u %s:%s -H \"Content-Type: application/json\" -X POST -d '{\"title\": \"%s\",\"body\": \"%s\",\"head\": \"%s\",\"base\": \"%s\"}' https://api.github.com/repos/%s/pulls" % (username, token, title, body, branch, master, repo) )
    else: 
      print ("open https://github.com/%s/compare/%s...%s" % (repo, master, branch))
      self.cli.executeRaw("open https://github.com/%s/compare/%s...%s" % (repo, master, branch))

    self.interface.ok("open a pull request on github")


  def finish(self, branch):
    self.interface.ok("gitcd feature finish")

    origin = self.getOrigin()

    self.cli.execute("git checkout %s" % (self.config.getMaster()))
    self.cli.execute("git pull %s %s" % (origin, self.config.getMaster()))
    self.cli.execute("git merge %s%s" % (self.config.getFeature(), branch))
    self.cli.execute("git push %s %s" % (origin, self.config.getMaster()))

    # push new tag
    currentDate = time.strftime("%Y.%m.%d%H%M")
    # need to handle commit message here, interactive shell execution could be a possiblity
    self.cli.execute("git tag -a -m 'release' %s%s" % (self.config.getTag(), currentDate))
    self.cli.execute("git push %s %s%s" % (origin, self.config.getTag(), currentDate))

    deleteFeatureBranch = self.interface.askFor("Delete your feature branch?",
      ["yes", "no"],
      "yes"
    )

    if deleteFeatureBranch == "yes":
      # delete feature branch locally and remote
      self.cli.execute("git branch -D %s%s" % (self.config.getFeature(), branch))
      self.cli.execute("git push %s :%s%s" % (origin, self.config.getFeature(), branch))
