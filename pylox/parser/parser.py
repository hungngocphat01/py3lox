from typing import List
from pylox.token import Token
from pylox.error_reporter import ErrorReporter
from pylox.ast import Expr, Stmt
from pylox.parser.state import ParserState
from pylox.parser.expression import ExpressionParser
from pylox.parser.statement import StatementParser
from pylox.parser.exc import ParseError

"""
Expression grammar
-------------------------
expression     → equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" ;

Statement grammar
-------------------------
program        → statement* EOF ;

statement      → exprStmt
               | printStmt ;

exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;
"""


class Parser:
    def __init__(self, tokens: List[Token], error_reporter: ErrorReporter):
        self.state = ParserState(tokens, error_reporter)
        self.expr_parser = ExpressionParser(self.state)
        self.stmt_parser = StatementParser(self.state, self.expr_parser)

    def parse(self) -> List[Stmt]:
        try:
            return self.stmt_parser.parse_program()
        except ParseError:
            return None
        
    def _parse_expr(self) -> Expr:
        try:
            return self.expr_parser.parse_expr()
        except ParseError:
            return None
        