from lexer  import Lexer
from parser import Parser
from interpreter import Interpreter

had_error = False
repl_engaged = False

if __name__ == '__main__':
  print('Welcome to susslang!')
  filename = input('Press ENTER to go to REPL, or type filename <-repl> below:\n> ')

  try:
    chrs = ''
    filenames = filename.split(' ')

    for filename in filenames:
      if filename == '-repl':
        repl_engaged = True
        continue

      f = open('src/' + filename)
      chrs += f.read()
      chrs += '\n'
      f.close()

    tokens = Lexer(chrs).lex()
    statements = Parser(tokens).parse()
    interpreter = Interpreter()
    interpreter.interpret(statements)

  except:
    repl_engaged = True
  
  if repl_engaged:
    interpreter = Interpreter(verbose=True)
    print('REPL Initiated.')
    while True:
      characters = input('> ')
      characters += '\n'
      try:
        tokens = Lexer(characters).lex() 
      except Lexer.LexerError:
        continue
      statements = Parser(tokens).parse()
      interpreter.interpret(statements)
