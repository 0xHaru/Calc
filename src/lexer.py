from __future__ import annotations

from token_ import Token, TokenType


class LexicalError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"Lexical error: {message}")


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def is_digit(self, char: str) -> bool:
        return char in "0123456789"

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: TokenType, literal: str) -> None:
        self.tokens.append(Token(type, literal))

    def consume_number(self) -> None:
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

        while self.is_digit(self.peek()):
            self.advance()

    def scan_token(self) -> None:
        char = self.advance()
        literal = self.source[self.start : self.current]

        match char:
            case "+":
                self.add_token(TokenType.PLUS, literal)
            case "-":
                self.add_token(TokenType.MINUS, literal)
            case "*":
                self.add_token(TokenType.STAR, literal)
            case "/":
                self.add_token(TokenType.SLASH, literal)
            case "^":
                self.add_token(TokenType.CARET, literal)
            case "(":
                self.add_token(TokenType.L_PAREN, literal)
            case ")":
                self.add_token(TokenType.R_PAREN, literal)
            # Ignore whitespace
            case " ":
                return
            case "\t":
                return
            case "\n":
                return
            case _:
                if not self.is_digit(char):
                    ch = self.source[self.current - 1]
                    raise LexicalError(f'invalid character "{ch}"')

                if char == "0" and self.is_digit(self.peek()):
                    raise LexicalError("leading zeros are not allowed")

                self.consume_number()
                literal = self.source[self.start : self.current]
                self.add_token(TokenType.NUMBER, literal)

    def tokenize(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.add_token(TokenType.EOL, "\0")
        return self.tokens
