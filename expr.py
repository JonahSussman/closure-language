from abc import ABC, abstractmethod

class Expr:
  class Visitor(ABC):
    @abstractmethod
    def visit_assign_expr(self, expr):   pass
    @abstractmethod
    def visit_listed_expr(self, expr):   pass
    @abstractmethod
    def visit_group_expr(self, expr):    pass
    @abstractmethod
    def visit_literal_expr(self, expr):  pass
    @abstractmethod
    def visit_variable_expr(self, expr): pass
    @abstractmethod
    def visit_cast_expr(self, expr):     pass
    @abstractmethod
    def visit_call_expr(self, expr):     pass
  
  class Listed:
    def __init__(self, operator, children=[]):
      self.operator = operator
      self.children = children
    def accept(self, visitor):
      return visitor.visit_listed_expr(self)

  class Assign:
    def __init__(self, name, value):
      self.name  = name
      self.value = value
    def accept(self, visitor):
      return visitor.visit_assign_expr(self)

  class Cast:
    def __init__(self, name, kind):
      self.name = name
      self.kind = kind
    def accept(self, visitor):
      return visitor.visit_cast_expr(self)

  class Call:
    def __init__(self, callee, paren, args):
      self.callee = callee
      self.paren  = paren
      self.args   = args
    def accept(self, visitor):
      return visitor.visit_call_expr(self)
  
  class Literal:
    def __init__(self, value):
      self.value = value
    def accept(self, visitor):
      return visitor.visit_literal_expr(self)

  class Grouping:
    def __init__(self, expression):
      self.expression = expression
    def accept(self, visitor):
      return visitor.visit_group_expr(self)
  
  class Variable:
    def __init__(self, name, value=None):
      self.name  = name
    def accept(self, visitor):
      return visitor.visit_variable_expr(self)
