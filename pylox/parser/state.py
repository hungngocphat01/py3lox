from dataclasses import dataclass
from typing import List 
from pylox.token import Token, TokenType
from pylox.error_reporter import ErrorReporter
from pylox.parser.exc import ParseError

@dataclass
class ParserState:
    tokens: List[Token]
    reporter: ErrorReporter
    position: int = 0


    def match_or_throw(self, t: TokenType, message: str):
        if self.check_current_type(t):
            return self.advance()

        raise self.error(self.peek(), message)

    def error(self, token: Token, msg: str):
        self.reporter.error_token(token, msg)
        return ParseError()

    def match_type(self, *args: TokenType):
        if any(self.check_current_type(t) for t in args):
            self.advance()
            return True
        return False

    def check_current_type(self, t: TokenType):
        if self.eof():
            return False
        return self.peek().token_type == t

    def advance(self):
        if not self.eof():
            self.position += 1
        return self.previous()

    def peek(self):
        return self.tokens[self.position]

    def previous(self):
        return self.tokens[self.position - 1]

    def eof(self):
        return self.peek().token_type == TokenType.EOF
    