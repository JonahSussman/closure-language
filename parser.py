from expr import Expr
from stmt import Stmt

class Parser:
  class ParserError(Exception):
    pass

  def __init__(self, tokens):
    self.tokens = tokens
    self.c_tok  = 0

  def match(self, *kinds):
    if self.c_tok == len(self.tokens):
      return False

    for kind in kinds:
      if kind == self.tokens[self.c_tok].kind:
        return True
    
    return False

  def error(self, token):
    print('Parser Error! Invalid token: %s' % (token))
    raise Parser.ParserError

  def declaration(self):
    try:
      if self.match('FUNCTION'):
        self.c_tok += 1
        return self.function('function')
      elif self.match('LET'):
        self.c_tok += 1
        return self.var_declaration()
      else:
        return self.statement()
    except Parser.ParserError:
      print(self.tokens)
      exit()
  
  def statement(self):
    if self.match('IF'):
      self.c_tok += 1
      return self.if_statement()
    elif self.match('WHILE'):
      self.c_tok += 1
      return self.while_statement()
    elif self.match('PRINT'):
      self.c_tok += 1
      return self.print_statement()
    elif self.match('RETURN'):
      self.c_tok += 1
      return self.return_statment()
    elif self.match('L_BRACE'):
      self.c_tok += 1
      return Stmt.Block(self.block())
    
    return self.expression_statment()

  def block(self):
    statements = []
    while not self.match('R_BRACE') and self.c_tok < len(self.tokens):
      statements.append(self.declaration())

    self.c_tok += 1
    return statements

  def function(self, like):
    if not self.match('ID'):
      raise Parser.ParserError
    name = self.tokens[self.c_tok].value
    self.c_tok += 1

    if not self.match('L_PAREN'):
      print('Expected \'(\' after function name')
      raise Parser.ParserError
    self.c_tok += 1

    params = []

    if not self.match('R_PAREN'):
      while True:
        if not self.match('ID'):
          print('Expected identifier in parameters.')
          raise Parser.ParserError
        params.append(self.tokens[self.c_tok])
        self.c_tok += 1

        if not self.match('COMMA'):
          break
        self.c_tok += 1

    if not self.match('R_PAREN'):
      print('Expected \')\' after function params')
      raise Parser.ParserError
    self.c_tok += 1

    if not self.match('L_BRACE'):
      print('Expected \'{\' before body')
      raise Parser.ParserError
    self.c_tok += 1

    body = self.block()
    return Stmt.Fn(name, params, body)
    
  def print_statement(self):
    value = self.expression()
    if not self.match('ENDLINE'):
      raise Parser.ParserError
    self.c_tok += 1
    return Stmt.Print(value)

  def return_statment(self):
    value = None
    if not self.match('ENDLINE'):
      value = self.expression()

    if not self.match('ENDLINE'):
      print('\\n must follow return value')
      raise Parser.ParserError
    
    self.c_tok += 1
    return Stmt.Return('return', value)

  def if_statement(self):
    if not self.match('L_PAREN'):
      raise Parser.ParserError
    self.c_tok += 1

    expression = self.expression()

    if not self.match('R_PAREN'):
      raise Parser.ParserError
    self.c_tok += 1

    then_branch = self.statement()
    else_branch = None
    if self.match('ELSE'):
      self.c_tok += 1
      else_branch = self.statement()

    return Stmt.If(expression, then_branch, else_branch)

  def while_statement(self):
    if not self.match('L_PAREN'):
      raise Parser.ParserError
    self.c_tok += 1
    
    expression = self.expression()

    if not self.match('R_PAREN'):
      raise Parser.ParserError
    self.c_tok += 1

    body = self.statement()

    return Stmt.While(expression, body)

  def expression_statment(self):
    value = self.expression()
    if not self.match('ENDLINE'):
      raise Parser.ParserError
    self.c_tok += 1
    return Stmt.Expression(value)

  def var_declaration(self):
    if not self.match('ID'):
      raise Parser.ParserError

    name = self.tokens[self.c_tok].value
    self.c_tok += 1

    initalizer = None
    if self.match('EQUAL'):
      self.c_tok += 1
      initalizer = self.expression()
    
    if not self.match('ENDLINE'):
      raise Parser.ParserError
    self.c_tok += 1

    return Stmt.Let(name, initalizer)

  def expression(self):
    return self.assignment()

  def assignment(self):
    expr = self.cast()
    if self.match('EQUAL'):
      self.c_tok += 1
      
      value = self.assignment()

      if isinstance(expr, Expr.Variable):
        return Expr.Assign(expr.name, value)
      else:
        raise Parser.ParserError
    
    return expr

  def cast(self):
    expr = self.equality()

    if self.match('CAST'):
      self.c_tok += 1
      kind = self.cast()
      return Expr.Cast(expr, kind)
    
    return expr

  def equality(self):
    expr = self.comparison()
    
    while self.match('BANG_EQUAL', 'EQUAL_EQUAL', 'AND', 'OR'):
      operator = self.tokens[self.c_tok].value
      self.c_tok += 1
      right = self.comparison()
      expr = Expr.Listed(operator, [expr, right])
    return expr

  def comparison(self):
    expr = self.addition()

    while self.match('LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL'):
      operator = self.tokens[self.c_tok].value
      self.c_tok += 1
      right = self.addition()
      expr = Expr.Listed(operator, [expr, right])
    return expr

  def addition(self):
    expr = self.multiplication()

    while self.match('PLUS', 'MINUS'):
      operator = self.tokens[self.c_tok].value
      self.c_tok += 1
      right = self.multiplication()
      expr = Expr.Listed(operator, [expr, right])
    return expr

    self.c_tok += 1
    return Expr.Literal(self.tokens[self.c_tok - 1].value)

  def multiplication(self):
    expr = self.exponentiation()
    while self.match('STAR', 'SLASH', 'MOD'):
      operator = self.tokens[self.c_tok].value
      self.c_tok += 1
      right = self.exponentiation()
      expr = Expr.Listed(operator, [expr, right])
    return expr

    self.c_tok += 1
    return Expr.Literal(self.tokens[self.c_tok - 1].value)

  def exponentiation(self):
    stack = [self.negation()]

    while self.match('CARET'):
      self.c_tok += 1
      stack.append(self.negation())

    while len(stack) > 1:
      right = stack.pop()
      left = stack.pop()
      stack.append(Expr.Listed('^', [left, right]))
    return stack[0]

  def negation(self):
    if self.match('MINUS', 'NOT', 'LN', 'LOG_10', 'SQRT', 'INPUT'):
      operator = self.tokens[self.c_tok].value
      self.c_tok += 1
      right = self.negation()
      return Expr.Listed(operator, [right])
    else:
      return self.custom_root()

  def custom_root(self):
    expr = self.logbase()

    while self.match('ROOT'):
      operator = self.tokens[self.c_tok].value
      self.c_tok += 1
      right = self.logbase()
      expr = Expr.Listed(operator, [expr, right])
    return expr

  def logbase(self):
    if self.match('LOG'):
      operator = self.tokens[self.c_tok].value
      self.c_tok += 1
      base = self.logbase()
      argument = self.logbase()
      return Expr.Listed(operator, [base, argument])
    else:
      return self.factorial()

  def factorial(self):
    expr = self.call()

    while self.match('BANG'):
      operator = self.tokens[self.c_tok].value
      self.c_tok += 1
      expr = Expr.Listed(operator, [expr])
    return expr

  def call(self):
    expr = self.primary()

    while True:
      if self.match('L_PAREN'):
        self.c_tok += 1
        expr = self.finish_call(expr)
      else:
        break
    return expr

  def finish_call(self, callee):
    arguments = []
    if not self.match('R_PAREN'):
      while True:
        arguments.append(self.expression())
        if not self.match('COMMA'):
          break
        self.c_tok += 1
    
    if not self.match('R_PAREN'):
      print('No \')\' after arguments!')
      raise Parser.ParserError

    paren = self.tokens[self.c_tok]
    self.c_tok += 1

    return Expr.Call(callee, paren, arguments)
    
  def primary(self):
    expr = None
    token_value = self.tokens[self.c_tok].value

    if self.match('ENDLINE'):
      self.c_tok -= 1
      expr = Expr.Literal(None)

    elif self.match('TRUE'):  expr = Expr.Literal(True)
    elif self.match('FALSE'): expr = Expr.Literal(False)
    elif self.match('NIL'):   expr = Expr.Literal(None)

    elif self.match('STRING'): expr = Expr.Literal(token_value[1:len(token_value)-1])
    elif self.match('NUM'): expr = Expr.Literal(float(token_value))
    elif self.match('KIND'): expr = Expr.Literal(token_value)
    
    elif self.match('ID'): expr = Expr.Variable(token_value)
      
    elif self.match('L_PAREN'):
      self.c_tok += 1
      expr = Expr.Grouping(self.expression())
      if not self.match('R_PAREN'):
        raise Parser.ParserError
    
    if not expr:
      raise Parser.ParserError

    self.c_tok += 1

    return expr

  def parse(self):
    statements = []

    while self.c_tok < len(self.tokens):
      statements.append(self.declaration())

    return statements
