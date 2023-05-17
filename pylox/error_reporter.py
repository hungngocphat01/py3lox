from pylox.token import Token, TokenType

class ErrorReporter:
    def __init__(self):
        self.had_error = False

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def error_token(self, token: Token, message: str):
        if token.token_type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, " at '{}'".format(token.lexeme), message)
    
    def report(self, line: int, where: str, message: str):
        print("[Line {}] Error {}: {}".format(line, where, message))
        self.had_error = True
        