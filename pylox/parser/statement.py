from typing import List 
from dataclasses import dataclass
from pylox.token import Token, TokenType
from pylox.ast.expr import Expr
from pylox.ast.stmt import Stmt, PrintStmt, ExpressionStmt
from pylox.parser.state import ParserState
from pylox.parser.expression import ExpressionParser

""" 
Statement grammar
-------------------------
program        → statement* EOF ;

statement      → exprStmt
               | printStmt ;

exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;
"""

@dataclass
class StatementParser:
    state: ParserState
    expr_parser: ExpressionParser

    def parse_program(self) -> List[Stmt]:
        statements: List[Stmt] = []
        
        while not self.state.eof():
            statements.append(self.parse_stmt())

        return statements

    def parse_stmt(self) -> Stmt:
        if self.state.match_type(TokenType.PRINT):
            return self.parse_print()
        
        return self.parse_expr_stmt()

    def parse_print(self) -> PrintStmt:
        expr = self.expr_parser.parse_expr()
        self.state.match_or_throw(TokenType.SEMICOLON, "Expected ; after value")
        return PrintStmt(expr)

    def parse_expr_stmt(self) -> ExpressionStmt:
        expr = self.expr_parser.parse_expr()
        self.state.match_or_throw(TokenType.SEMICOLON, "Expected ; after value")
        return ExpressionStmt(expr)
