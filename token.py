from typing import NamedTuple

tok_types = {
  r'[\ \t]+': None,
  r'#.*\n':   None,

  r'\n': 'ENDLINE',
  r':':  'COLON',
  r'\|': 'BAR',
  r'\~': 'NOT',

  r'->': 'CAST',

  r'\+': 'PLUS',
  r'\-': 'MINUS',
  r'\*': 'STAR',
  r'\/': 'SLASH',
  r'\^': 'CARET',
  r'\%': 'MOD',
  r'\,': 'COMMA',

  r'_root': 'ROOT',
  r'sqrt':  'SQRT',

  r'log_': 'LOG',
  r'log':  'LOG_10',
  r'ln':   'LN',
  
  r'\(': 'L_PAREN',
  r'\)': 'R_PAREN',
  r'\{': 'L_BRACE',
  r'\}': 'R_BRACE',

  r'==':  'EQUAL_EQUAL',
  r'!=':  'BANG_EQUAL',
  r'<=':  'LESS_EQUAL',
  r'>=':  'GREATER_EQUAL',
  r'<':   'LESS',
  r'>':   'GREATER',
  r'and': 'AND',
  r'or':  'OR',

  r'!':  'BANG',
  r'=':  'EQUAL',

  r'true':  'TRUE',
  r'false': 'FALSE',
  r'nil':   'NIL',

  r'(str)|(num)|(bool)' : 'KIND',

  r'let':    'LET',
  r'if':     'IF',
  r'else':   'ELSE',
  r'while':  'WHILE',
  r'fn':     'FUNCTION',
  r'return': 'RETURN', 

  r'print': 'PRINT',
  r'input': 'INPUT',

  r'import': 'IMPORT',

  r'\'(.*?)\'': 'STRING',
  r'[A-Za-z\_]+': 'ID',
  
  r'((\d+(\.\d*)?)|(\.\d+))' : 'NUM'
}

class Token(NamedTuple):
  value: str
  kind:  str

  def __str__(self):
    return '(%s, %s)' % (self.value, self.kind)

  def __repr__(self):
    return self.__str__()