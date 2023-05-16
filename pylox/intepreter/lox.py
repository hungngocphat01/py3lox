from typing import List
from pylox.lexer.scanner import Scanner
from pylox.token import Token
from pylox.error_reporter import ErrorReporter

class Lox:
    """The Lox intepreter"""
    
    def __init__(self):
        self.error_reporter = ErrorReporter()

    def run(self, source: str):
        """Run one line of the Lox source code

        Parameters
        ----------
        source : str
            The source code to run
        """

        scanner = Scanner(source, self.error_reporter)
        tokens: List[Token] = scanner.scan_tokens()

        for token in tokens:
            print(token)
    