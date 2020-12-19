from abc import ABC, abstractmethod

class Stmt:
  class Visitor(ABC):
    @abstractmethod
    def visit_expression_stmt(self, stmt): pass
    @abstractmethod
    def visit_block_stmt(self, stmt):      pass
    @abstractmethod
    def visit_print_stmt(self, stmt):      pass
    @abstractmethod
    def visit_let_stmt(self, stmt):        pass
    @abstractmethod
    def visit_if_stmt(self, stmt):         pass
    @abstractmethod
    def visit_while_stmt(self, stmt):      pass
    @abstractmethod
    def visit_fn_stmt(self, stmt):         pass
    @abstractmethod
    def visit_return_stmt(self, expr):   pass

  class Expression:
    def __init__(self, expression):
      self.expression = expression
    def accept(self, visitor):
      return visitor.visit_expression_stmt(self)

  class Block:
    def __init__(self, statements):
      self.statements = statements
    def accept(self, visitor):
      return visitor.visit_block_stmt(self)

  class Print:
    def __init__(self, expression):
      self.expression = expression
    def accept(self, visitor):
      return visitor.visit_print_stmt(self)
    
  class Return:
    def __init__(self, keyword, value):
      self.keyword = keyword
      self.value = value
    def accept(self, visitor):
      return visitor.visit_return_stmt(self)

  class Let:
    def __init__(self, name, initializer):
      self.name = name
      self.initializer = initializer
    def accept(self, visitor):
      return visitor.visit_let_stmt(self)

  class Fn:
    def __init__(self, name, params, body):
      self.name = name
      self.body = body
      self.params = params
    def accept(self, visitor):
      return visitor.visit_fn_stmt(self)

  class If:
    def __init__(self, condition, then_branch, else_branch):
      self.condition = condition
      self.then_branch = then_branch
      self.else_branch = else_branch
    def accept(self, visitor):
      return visitor.visit_if_stmt(self)

  class While:
    def __init__(self, condition, body):
      self.condition = condition
      self.body = body
    def accept(self, visitor):
      return visitor.visit_while_stmt(self)