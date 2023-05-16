from pylox.token import Token, TokenType
from pylox.ast.expr import Unary, Literal, Grouping, Binary
from pylox.ast.ast_printer import AstPrinter

expr = Binary(
    Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
    Token(TokenType.STAR, "*", None, 1),
    Grouping(Literal(45.67)),
)

printer = AstPrinter()
print(printer.print(expr))
