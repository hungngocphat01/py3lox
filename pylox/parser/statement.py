from typing import List 
from dataclasses import dataclass
from pylox.token import TokenType
from pylox.ast.stmt import Stmt, PrintStmt, ExpressionStmt, VarStmt
from pylox.parser.state import ParserState
from pylox.parser.expression import ExpressionParser

""" 
Statement grammar
-------------------------
program        → statement* EOF ;

declStmt       → varDecl
               | statement

varDecl        → "var" IDENT ("=" expression)? ";"

statement      → exprStmt
               | printStmt

declStmt       → varDeclStmt ";"

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
            statements.append(self.parse_declaration())

        return statements
    
    def parse_declaration(self) -> Stmt:
        if self.state.match_type(TokenType.VAR):
            return self.parse_var_decl()
        
        return self.parse_stmt()
    
    def parse_var_decl(self) -> Stmt:
        var_name = self.state.match_or_throw(TokenType.IDENT, "Expect variable name")

        initializer = None 
        if self.state.match_type(TokenType.EQ):
            initializer = self.expr_parser.parse_expr()
        
        self.state.match_or_throw(TokenType.SEMICOLON, "Expect ; after variable declaration")
        
        return VarStmt(var_name, initializer)


    def parse_stmt(self) -> Stmt:
        if self.state.match_type(TokenType.PRINT):
            return self.parse_print()
        
        return self.parse_expr_stmt()

    def parse_print(self) -> Stmt:
        expr = self.expr_parser.parse_expr()
        self.state.match_or_throw(TokenType.SEMICOLON, "Expected ; after value")
        return PrintStmt(expr)

    def parse_expr_stmt(self) -> Stmt:
        expr = self.expr_parser.parse_expr()
        self.state.match_or_throw(TokenType.SEMICOLON, "Expected ; after value")
        return ExpressionStmt(expr)
