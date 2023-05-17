from typing import List
from pylox.token import Token, TokenType
from pylox.ast.expr import Expr, Binary, Unary, Literal, Grouping
from pylox.parser.exc import ParseError
from pylox.error_reporter import ErrorReporter

"""
expression     → equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" ;
"""

class Parser:
    def __init__(self, tokens: List[Token], error_reporter: ErrorReporter):
        self.tokens = tokens 
        self.position = 0
        self.reporter = error_reporter
    
    def parse(self) -> Expr:
        try:
            return self.parse_expr()
        except ParseError:
            return None
    
    def parse_expr(self) -> Expr:
        return self.parse_equality()

    def parse_equality(self) -> Binary:
        expr = self.parse_comparison()

        while self.match_type(TokenType.EQ_EQ, TokenType.BANG_EQ):
            op = self.previous()
            right = self.parse_comparison()
            expr = Binary(expr, op, right)
        
        return expr
    
    def parse_comparison(self) -> Binary:
        expr = self.parse_term()

        while self.match_type(TokenType.LESS, TokenType.LESS_EQ, TokenType.GREATER, TokenType.GREATER_EQ):
            op = self.previous()
            right = self.parse_term()
            expr = Binary(expr, op, right)
        
        return expr
    
    def parse_term(self) -> Binary:
        expr = self.parse_factor()

        while self.match_type(TokenType.PLUS, TokenType.MINUS):
            op = self.previous()
            right = self.parse_factor()
            expr = Binary(expr, op, right)
        
        return expr
    
    def parse_factor(self) -> Binary:
        expr = self.parse_unary()

        while self.match_type(TokenType.STAR, TokenType.SLASH):
            op = self.previous()
            right = self.parse_unary()
            expr = Binary(expr, op, right)
        
        return expr
    
    def parse_unary(self) -> Unary:
        while self.match_type(TokenType.BANG, TokenType.MINUS):
            op = self.previous()
            right = self.parse_primary()
            return Unary(op, right)

        return self.parse_primary()
        
    def parse_primary(self) -> Expr:
        if self.match_type(TokenType.FALSE):
            return Literal(False) 
        
        if self.match_type(TokenType.TRUE):
            return Literal(True) 

        if self.match_type(TokenType.NIL):
            return Literal(None)

        if self.match_type(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal) 
        
        if self.match_type(TokenType.LEFT_PAREN):
            expr = self.parse_expr()
            self.match_or_throw(TokenType.RIGHT_PAREN, "Missing closing parenthesis")
            return Grouping(expr)
        
        raise self.error(self.peek(), "Expected expression")


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