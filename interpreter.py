import math
from expr import Expr
from stmt import Stmt
from environment import Environment
from suss_function import SussFunction, Clock, Return

class Interpreter(Expr.Visitor, Stmt.Visitor):
  def __init__(self, verbose = False):
    self.globs = Environment()

    self.globs.define('clock', Clock())

    self.env = self.globs
    self.verbose = verbose

  def interpret(self, statements):
    try:
      for stmt in statements:
        self.execute(stmt)
    except RuntimeError:
      print('Implement Runtime error handling!')

  def execute(self, stmt):
    stmt.accept(self)

  def evaluate(self, expr):
    return expr.accept(self)

  def is_truthy(self, obj):
    if not obj: 
      return False
    if isinstance(obj, bool): 
      return obj
    if isinstance(obj, float):
      if obj == 0:
        return False
      else:
        return True
    if isinstance(obj, str):
      if obj == '0':
        return False
      else:
        return True

    return True

  def is_equal(self, a, b):
    if a == None and b == None: return True
    if a == None:               return False

    return a == b 

  def visit_expression_stmt(self, stmt):
    value = self.evaluate(stmt.expression)
    if self.verbose:
      print(value)
    return None

  def visit_fn_stmt(self, stmt):
    function = SussFunction(stmt, self.env)
    self.env.define(stmt.name, function)
    return None

  def visit_print_stmt(self, stmt):
    value = self.evaluate(stmt.expression)
    print(value)
    return None

  def visit_return_stmt(self, stmt):
    value = None
    if stmt.value != None:
      value = self.evaluate(stmt.value)

    raise Return(value)

  def visit_block_stmt(self, stmt):
    self.excecute_block(stmt.statements, Environment(self.env))
    return None

  def visit_if_stmt(self, stmt):
    if self.is_truthy(self.evaluate(stmt.condition)):
      self.execute(stmt.then_branch)
    elif stmt.else_branch != None:
      self.execute(stmt.else_branch)                       
    return None

  def visit_while_stmt(self, stmt):
    while self.is_truthy(self.evaluate(stmt.condition)):
      self.execute(stmt.body)
    return None

  def excecute_block(self, statements, env):
    previous = self.env
    try:
      self.env = env
      for statement in statements:
        self.execute(statement)
    finally:
      self.env = previous

  def visit_let_stmt(self, stmt):
    value = None

    if stmt.initializer != None:
      value = self.evaluate(stmt.initializer)
    
    self.env.define(stmt.name, value)
    if self.verbose:
      print('%s <- %s' % (stmt.name, value))
    return None

  def visit_literal_expr(self, expr):
    return expr.value

  def visit_group_expr(self, expr):
    return self.evaluate(expr.expression)

  def visit_variable_expr(self, expr):
    return self.env.get(expr.name)

  def visit_assign_expr(self, expr):
    value = self.evaluate(expr.value)
    self.env.assign(expr.name, value)
    return value

  def visit_cast_expr(self, expr):
    value = self.evaluate(expr.name)

    if expr.kind.value == 'str':
      return str(value)
    elif expr.kind.value == 'num':
      return float(value)
    elif expr.kind.value == 'bool':
      value = value.lower()
      return bool(value)

  def visit_call_expr(self, expr):
    callee = self.evaluate(expr.callee)

    arguments = []
    for arg in expr.args:
      arguments.append(self.evaluate(arg))

    if not isinstance(callee, SussFunction):
      print('Error! Only able to call functions!')
      raise RuntimeError

    if len(arguments) != callee.arity():
      print('Expected %s arguments, but got %s.' % (callee.arity(), len(arguments)))

    return callee.call(self, arguments)

  def visit_listed_expr(self, expr):
    results = []
    op = expr.operator

    for child in expr.children:
      results.append(self.evaluate(child))
      
    left = results[0]
    if len(results) > 1:
      right =  results[1]

    if op == '~':
      return not self.is_truthy(left)
    elif op == 'and':
      return self.is_truthy(left) and self.is_truthy(right)
    elif op == 'or':
      return self.is_truthy(left) or self.is_truthy(right)
    elif op == '!':
      fac, n = 1, left
      while n > 0:
        fac *= n
        n -= 1
      return fac
    elif op == '+':
      output = results[0]
      if isinstance(output, str):
        for term in results[1:len(results)]:
          output += str(term)
      else:   
        for term in results[1:len(results)]:
          output += term
      return output
    elif op == '-':
      if len(results) == 1:
        return -results[0]
      else:
        output = results[0]
        for term in results[1:len(results)]:
          output -= term
        return output
    elif op == '*':
      output = results[0]
      for term in results[1:len(results)]:
        output *= term
      return output
    elif op == '/':
      output = results[0]
      for term in results[1:len(results)]:
        output /= term
      return output
    elif op == '%':
      return results[0] % results[1]
    elif op == '^':
      return math.pow(left, right)
    elif op == '>':
      return left > right
    elif op == '<':
      return left < right
    elif op == '>=':
      return left >= right
    elif op == '<=':
      return left <= right
    elif op == '!=':
      return not self.is_equal(left, right)
    elif op == '==':
      return self.is_equal(left, right)
    elif op in ['log', 'ln', 'log_']:
      if op == 'log':
        return math.log10(left)
      elif op == 'ln':
        return math.log(left)
      elif op == 'log_':
        return math.log(right, left)
    elif op in ['_root', 'sqrt']:
      if op == '_root':
        return math.pow(right, (1/left))
      elif op == 'sqrt':
        return math.sqrt(left)
    elif op == 'input':
      return input(left)
