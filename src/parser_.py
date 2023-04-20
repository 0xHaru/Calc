from __future__ import annotations

from ast_ import ASTNode, BinaryExpr, Number, UnaryExpr
from token_ import Token, TokenType


class SyntaxError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"Syntax error: {message}")


# Grammar:
# expression ::= term ( ("+" | "-") term )*
# term       ::= factor ( ("*" | "/") factor )*
# factor     ::= ( "+" | "-" ) factor | primary
# primary    ::= number | "(" expression ")"
class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def peek(self) -> Token:
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        return self.tokens[self.current].type == TokenType.EOL

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]

    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.peek().type == type:
                return True
        return False

    def parse(self) -> ASTNode:
        result = self.expression()

        if not self.match(TokenType.EOL):
            ch = self.peek().literal
            raise SyntaxError(f'expected end of line but "{ch}" was found')

        return result

    # expression ::= term ( ("+" | "-") term )*
    def expression(self) -> ASTNode:
        expr = self.term()

        while not self.is_at_end() and self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.advance()
            right = self.term()
            expr = BinaryExpr(operator, left=expr, right=right)

        return expr

    # term ::= factor ( ("*" | "/") factor )*
    def term(self) -> ASTNode:
        expr = self.factor()

        while not self.is_at_end() and self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.advance()
            right = self.factor()
            expr = BinaryExpr(operator, left=expr, right=right)

        return expr

    # factor ::= ( "+" | "-" ) factor | primary
    def factor(self) -> ASTNode:
        if self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.advance()
            right = self.factor()
            return UnaryExpr(operator, right=right)

        return self.primary()

    # primary ::= number | "(" expression ")"
    def primary(self) -> ASTNode:
        if self.match(TokenType.NUMBER):
            number = self.advance()
            return Number(value=float(number.literal))

        if self.match(TokenType.L_PAREN):
            self.advance()  # Consume L_PAREN
            expr = self.expression()

            if not self.match(TokenType.R_PAREN):
                raise SyntaxError("missing closing parenthesis")

            self.advance()  # Consume R_PAREN
            return expr

        if self.is_at_end():
            raise SyntaxError("unexpected end of line")

        raise SyntaxError(f'unexpected character "{self.peek().literal}"')
