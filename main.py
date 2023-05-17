from pylox.token import Token, TokenType
from pylox.ast.expr import Unary, Literal, Grouping, Binary
from pylox.ast.ast_printer import AstPrinter
from pylox.lexer.scanner import Scanner
from pylox.parser.parser import Parser
from pylox.error_reporter import ErrorReporter

source = "123 456 789"
error_reporter = ErrorReporter()
scanner = Scanner(source, error_reporter)
tokens = scanner.scan_tokens()

parser = Parser(tokens, error_reporter)
ast = parser.parse()

printer = AstPrinter()
print(printer.print(ast))
