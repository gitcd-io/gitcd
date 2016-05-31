from gitcd.Git.Command import Command

class Init(Command):

  # no special subcommands, only run which is meant to be default

  def run(self):
    self.config.setMaster(
      self.interface.askFor("Branch name for production releases?",
      False,
      self.config.getMaster())
    )

    self.config.setFeature(
      self.interface.askFor("Branch name for feature development?",
      False,
      self.config.getFeature())
    )

    self.config.setTest(
      self.interface.askFor("Branch name for test releases?",
      False,
      self.config.getTest())
    )

    self.config.setTag(
      self.interface.askFor("Version tag prefix?",
      False,
      self.config.getTag())
    )

    self.config.write()