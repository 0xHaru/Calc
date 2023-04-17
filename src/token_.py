from enum import Enum


class TokenType(Enum):
    NUMBER = 1

    PLUS = 2
    MINUS = 3
    STAR = 4
    SLASH = 5
    L_PAREN = 6
    R_PAREN = 7

    EOL = 8


class Token:
    def __init__(self, type: TokenType, literal: str) -> None:
        self.type = type
        self.literal = literal

    def __repr__(self) -> str:
        type = str(self.type).split(".")[1]

        if self.type == TokenType.NUMBER:
            return f"{type}={self.literal}"

        return type
