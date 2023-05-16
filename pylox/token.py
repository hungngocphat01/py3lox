from enum import Enum
from dataclasses import dataclass

TokenType = Enum(
    "TokenType",
    [
        # One-character tokens
        "LEFT_PAREN",
        "RIGHT_PAREN",
        "LEFT_BRACE",
        "RIGHT_BRACE",
        "COMMA",
        "DOT",
        "MINUS",
        "PLUS",
        "SEMICOLON",
        "SLASH",
        "STAR",
        # One or two character tokens
        "BANG",
        "BANG_EQ",
        "EQ",
        "EQ_EQ",
        "GREATER",
        "GREATER_EQ",
        "LESS",
        "LESS_EQ",
        # Literals
        "IDENT",
        "STRING",
        "NUMBER",
        # Keywords
        "AND",
        "CLASS",
        "ELSE",
        "FALSE",
        "FUN",
        "FOR",
        "IF",
        "NIL",
        "OR",
        "PRINT",
        "RETURN",
        "SUPER",
        "THIS",
        "TRUE",
        "VAR",
        "WHILE",
        "EOF",
    ],
)

@dataclass
class Token:
    token_type: TokenType
    lexeme: str 
    literal: object
    line: int

    def to_string(self) -> str:
        return "{} {} {}".format(self.token_type, self.lexeme, self.literal)
    
    