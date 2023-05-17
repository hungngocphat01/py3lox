from typing import List
from pylox.token import Token
from pylox.ast.expr import Expr
from pylox.error_reporter import ErrorReporter
from pylox.lexer import Scanner
from pylox.parser import Parser
from pylox.intepreter.evaluate import Evaluator

class Intepreter:
    def intepret(self, source: str) -> object:
        tokens, e = self.lex(source)
        if e.had_error:
            return
        
        ast, e = self.parse(tokens)
        if e.had_error:
            return 
        
        return self.evaluate(ast)
    
    def lex(self, source: str):
        error_reporter = ErrorReporter()
        scanner = Scanner(source, error_reporter)
        tokens = scanner.scan_tokens()

        return tokens, error_reporter
    
    def parse(self, tokens: List[Token]):
        error_reporter = ErrorReporter()
        parser = Parser(tokens, error_reporter)
        ast = parser.parse()

        return ast, error_reporter
    
    def evaluate(self, ast: Expr):
        evaluator = Evaluator()
        return evaluator.evaluate(ast)
    
    def stringify(self, obj: object):
        s = str(obj)
        if isinstance(obj, float):
            s.endswith(".0")
            s = s[:s.find(".0")]
        return s
