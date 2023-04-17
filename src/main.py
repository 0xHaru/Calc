from lexer import Lexer
from parser_ import Parser

print("Press CTRL + D to quit")

while True:
    try:
        lexer = Lexer(input("> "))
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        # print(tokens)
        # print(ast)
        print(ast.eval())
    except EOFError:
        print()
        exit(0)
    except Exception as e:
        print(e)
