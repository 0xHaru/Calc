from __future__ import annotations

from token_ import Token, TokenType


class ASTNode:
    def eval(self) -> float:
        pass


class BinaryExpr(ASTNode):
    def __init__(self, operator: Token, left: ASTNode, right: ASTNode) -> None:
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.operator}({self.left},{self.right})"

    def eval(self) -> float:
        match self.operator.type:
            case TokenType.PLUS:
                return self.left.eval() + self.right.eval()
            case TokenType.MINUS:
                return self.left.eval() - self.right.eval()
            case TokenType.STAR:
                return self.left.eval() * self.right.eval()
            case TokenType.SLASH:
                return self.left.eval() / self.right.eval()
            case _:
                raise Exception("Invalid token type")


class UnaryExpr(ASTNode):
    def __init__(self, operator: Token, right: ASTNode) -> None:
        self.operator = operator
        self.right = right

    def __repr__(self) -> str:
        return f"{self.operator}({self.right})"

    def eval(self) -> float:
        match self.operator.type:
            case TokenType.PLUS:
                return +self.right.eval()
            case TokenType.MINUS:
                return -self.right.eval()
            case _:
                raise Exception("Invalid token type")


class Literal(ASTNode):
    def __init__(self, value: float) -> None:
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)

    def eval(self) -> float:
        return self.value
