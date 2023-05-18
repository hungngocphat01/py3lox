from typing import List

from pylox import Token, Expr, Stmt, ErrorReporter
from pylox.lexer import Scanner
from pylox.parser import Parser
from pylox.intepreter.expression import ExprEvaluator
from pylox.intepreter.statement import StmtEvaluator
from pylox.intepreter.environment import Environment

class Intepreter:
    def __init__(self):
        self.env = Environment()
        self.error_reporter = ErrorReporter()
        self.expr_evaluator = ExprEvaluator(self.env)
        self.stmt_evaluator = StmtEvaluator(self.expr_evaluator, self.env)

    def intepret(self, source: str) -> object:
        tokens, e = self.lex(source)
        if e.had_error:
            return None
        
        statements, e = self.parse(tokens)
        if e.had_error:
            return None
        
        return self.evaluate(statements)
    
    def _intepret_expr(self, source: str) -> object:
        tokens, e = self.lex(source)
        if e.had_error:
            return None
        
        ast, e = self._parse_expr(tokens)
        if e.had_error:
            return None
        
        return self.evaluate_expr(ast)
    
    def lex(self, source: str):
        error_reporter = ErrorReporter()
        scanner = Scanner(source, error_reporter)
        tokens = scanner.scan_tokens()

        return tokens, error_reporter
    
    def parse(self, tokens: List[Token]):
        error_reporter = ErrorReporter()
        parser = Parser(tokens, error_reporter)
        statements = parser.parse()

        return statements, error_reporter
    
    def _parse_expr(self, tokens: List[Token]):
        error_reporter = ErrorReporter()
        parser = Parser(tokens, error_reporter)
        # pylint: disable=W0212
        statements = parser._parse_expr()

        return statements, error_reporter
    
    def evaluate_expr(self, ast: Expr):
        return self.expr_evaluator.evaluate(ast)

    def evaluate(self, statements: List[Stmt]):
        for stmt in statements:
            self.stmt_evaluator.evaluate(stmt)
