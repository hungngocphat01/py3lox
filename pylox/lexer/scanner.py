from typing import List
from pylox.token import Token, TokenType
from pylox.error_reporter import ErrorReporter

ONE_CHAR_TOKENS = {
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
    "-": TokenType.MINUS,
    "+": TokenType.PLUS,
    ";": TokenType.SEMICOLON,
    "*": TokenType.STAR,
}

CONDITIONAL_TOKENS = {
    "!": (TokenType.BANG, ("=", TokenType.BANG_EQ)),
    "=": (
        TokenType.EQ,
        ("=", TokenType.EQ_EQ),
    ),
    "<": (
        TokenType.LESS,
        ("=", TokenType.LESS_EQ),
    ),
    ">": (
        TokenType.GREATER,
        ("=", TokenType.GREATER_EQ),
    ),
}

KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF, 
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE
}


class Scanner:
    """The Lox lexer"""

    def __init__(self, source: str, error_reporter: ErrorReporter):
        self.source: str = source
        self.tokens: List[Token] = []
        self.reporter = error_reporter

        self.state = Scanner.ScannerStates(source)

    def scan_tokens(self) -> List[Token]:
        while not self.state.eof():
            self.state.start = self.state.current
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.state.line))
        return self.tokens

    def _scan_token(self):
        c = self.state.advance()

        match c:
            case c if c in ONE_CHAR_TOKENS:
                self._add_token(ONE_CHAR_TOKENS[c], None)
            case c if c in CONDITIONAL_TOKENS:
                token_entry = CONDITIONAL_TOKENS[c]
                if self.state.advance_match("="):
                    token_type: TokenType = token_entry[1][1]
                else:
                    token_type: TokenType = token_entry[0]

                self._add_token(token_type, None)
            case "/":
                if self.state.advance_match("/"):
                    while self.state.peek() != "\n" and not self.state.eof():
                        self.state.advance()
                else:
                    self._add_token(TokenType.SLASH, None)

            case " " | "\t" | "\r":
                # Harmless white spaces
                ...
            case "\n":
                self.state.line += 1
            case '"':
                self._handle_string()
            case c if c.isdigit():
                self._handle_numeric()
            case c if (c.isalpha() or c == "_"):
                self._handle_ident()
            case _:
                self.reporter.error(self.state.line, f"Illegal character {c}")

    def _handle_string(self):
        # Search for the end of the string
        begin_string_line = self.state.line
        while self.state.peek() != '"' and not self.state.eof():
            if self.state.peek() == "\n":
                self.state.line += 1
            self.state.advance()

        # Now `current` should point at the end quote
        if self.state.eof():
            self.reporter.error(begin_string_line, "Unterminated string")
            return

        substr = self.source[self.state.start + 1 : self.state.current]

        # Skip pass the end quote
        self.state.advance()
        self._add_token(TokenType.STRING, substr)

    def _handle_numeric(self):
        while self.state.peek().isdigit():
            self.state.advance()

        if self.state.peek() == "." and self.state.peek_next().isdigit():
            self.state.advance()
            while self.state.peek().isdigit():
                self.state.advance()

        # The `current` pointer now point to a non-numeric character
        num = float(self.source[self.state.start : self.state.current])
        self._add_token(TokenType.NUMBER, num)

    def _handle_ident(self):
        while not self.state.eof():
            c = self.state.peek()
            if not (c.isalnum() or c == "_"):
                break 
            self.state.advance()
        
        # Now `current` should point to the character after the identifier
        ident = self.state.source[self.state.start : self.state.current]
        if ident in KEYWORDS:
            self._add_token(KEYWORDS[ident], None)
        else:
            self._add_token(TokenType.IDENT, None)

    def _add_token(self, token: TokenType, literal: object):
        text = self.source[self.state.start : self.state.current]
        self.tokens.append(Token(token, text, literal, self.state.line))

    class ScannerStates:
        """Just an inner class for to encapsulate non-public functions"""

        def __init__(self, source: str):
            self.start: int = 0
            self.current: int = 0
            self.line: int = 0

            self.source = source

        def peek(self):
            if self.current >= len(self.source):
                return "\0"
            return self.source[self.current]

        def advance(self):
            """Get current char and advance the pointer"""
            current_char = self.source[self.current]
            self.current += 1
            return current_char

        def advance_match(self, expected: str) -> bool:
            """Advance only if the next character matches"""
            if self.eof():
                return False
            if self.source[self.current] != expected:
                return False

            self.current += 1
            return True

        def peek_next(self):
            if self.current + 1 >= len(self.source):
                return "\0"
            return self.source[self.current + 1]

        def eof(self) -> bool:
            """Check if we reached end of the source file"""
            return self.current >= len(self.source)
