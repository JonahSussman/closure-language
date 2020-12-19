from environment import Environment
import time

class Return(Exception):
  def __init__(self, value):
    self.value = value

class SussFunction:
  def __init__(self, declaration=None, closure=None):
    self.declaration = declaration
    self.closure = closure
  def call(self, interpreter, arguments):
    env = Environment(self.closure)

    for i in range(0, len(self.declaration.params)):
      env.define(self.declaration.params[i].value, arguments[i])
    
    try:
      interpreter.excecute_block(self.declaration.body, env)
    except Return as r:
      return r.value
    return None
  def arity(self):
    return len(self.declaration.params)
  def __str__(self):
    return '<FUNCTION %s>' % self.declaration.name

class Clock(SussFunction):
  def arity(self):
    return 0
  def call(self, interpreter, arguments):
    return int(round(time.time() * 1000))
  def __str__(self):
    return '<CLOCK FUNCTION>'

    