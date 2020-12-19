class Environment:
  def __init__(self, enclosing=None):
    self.values = {}
    self.enclosing = enclosing

  def define(self, name, value):
    self.values[name] = value

  def get(self, name):
    if name in self.values.keys():
      return self.values[name]

    if self.enclosing != None:
      return self.enclosing.get(name)
    
    raise RuntimeError

  def assign(self, name, value):
    if name in self.values:
      self.values[name] = value
      return
    elif self.enclosing != None:
      self.enclosing.assign(name, value)
      return
    else:
      raise RuntimeError