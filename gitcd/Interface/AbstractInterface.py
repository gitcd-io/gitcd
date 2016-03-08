class AbstractInterface(object):

  def writeOut(self, msg: str):
    print(msg)
    return True

  def error(self, msg: str):
    return self.writeOut(msg)

  def warning(self, msg: str):
    return self.writeOut(msg)

  def header(self, msg: str):
    return self.writeOut(msg)

  def info(self, msg: str):
    return self.writeOut(msg)

  def ok(self, msg: str):
    return self.writeOut(msg)

  def askFor(self, prompt: str, options: list = False, default: str = False):
    raise Exception("Not implemented in abstract class gitcds.Interface.AbstractInterface.AbstractInterface")