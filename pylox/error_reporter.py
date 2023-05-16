class ErrorReporter:
    def __init__(self):
        self.had_error = False

    def error(self, line: int, message: str):
        self.report(line, "", message)
    
    def report(self, line: int, where: str, message: str):
        print("[Line {}] Error {}: {}".format(line, where, message))
        self.had_error = True
        