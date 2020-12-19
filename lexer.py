import re
from token import Token, tok_types

class Lexer:
  class LexerError(Exception):
    pass
  def __init__(self, chars):
    self.chars = chars

  def lex(self):
    loc = 0
    token_list = []
    import_flag = False
    has_pasted  = False

    while loc < len(self.chars):
      match = None
      offset = 0

      for r_expr in tok_types:
        pattern = re.compile(r_expr)
        match = pattern.match(self.chars, loc)

        if match:
          value = match.group(0)
          kind  = tok_types[r_expr]
          
          if kind == 'IMPORT':
            import_flag = True
          elif kind == 'ID' and import_flag:
            try:
              chrs = ''
              f = open('src/' + value)
              chrs += f.read()
              chrs += '\n'
              f.close()

              offset = len(value)
              self.chars = self.chars[:(loc - 7)] + chrs + self.chars[(loc + offset):]
              has_pasted = True

            except Exception as e:
              print('Import error! %s' % (e))
              exit()
          elif kind != None:
            token_list.append(Token(value, kind))
          break

      if not match:
        return self.error(loc)

      if has_pasted:
        loc = match.end(0) - 7 - offset
        import_flag = False
        has_pasted  = False
      else:
        loc = match.end(0)
    
    return token_list

  def error(self, loc):
    print('Lexer Error! Location: %s Character: %s' % (loc, self.chars[loc]))
    raise Lexer.LexerError
