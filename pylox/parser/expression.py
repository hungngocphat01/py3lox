from pylox.token import TokenType
from pylox.ast.expr import BinaryExpr, UnaryExpr, LiteralExpr, GroupingExpr, VariableExpr, Expr
from pylox.parser.state import ParserState

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
               | "(" expression ")"
               | IDENT ;
"""

class ExpressionParser:
    def __init__(self, state: ParserState):
        self.state = state

    def parse_expr(self) -> Expr:
        return self.parse_equality()

    def parse_equality(self) -> BinaryExpr:
        expr = self.parse_comparison()

        while self.state.match_type(TokenType.EQ_EQ, TokenType.BANG_EQ):
            op = self.state.previous()
            right = self.parse_comparison()
            expr = BinaryExpr(expr, op, right)

        return expr

    def parse_comparison(self) -> BinaryExpr:
        expr = self.parse_term()

        while self.state.match_type(
            TokenType.LESS,
            TokenType.LESS_EQ,
            TokenType.GREATER,
            TokenType.GREATER_EQ,
        ):
            op = self.state.previous()
            right = self.parse_term()
            expr = BinaryExpr(expr, op, right)

        return expr

    def parse_term(self) -> BinaryExpr:
        expr = self.parse_factor()

        while self.state.match_type(TokenType.PLUS, TokenType.MINUS):
            op = self.state.previous()
            right = self.parse_factor()
            expr = BinaryExpr(expr, op, right)

        return expr

    def parse_factor(self) -> BinaryExpr:
        expr = self.parse_unary()

        while self.state.match_type(TokenType.STAR, TokenType.SLASH):
            op = self.state.previous()
            right = self.parse_unary()
            expr = BinaryExpr(expr, op, right)

        return expr

    def parse_unary(self) -> UnaryExpr:
        while self.state.match_type(TokenType.BANG, TokenType.MINUS):
            op = self.state.previous()
            right = self.parse_primary()
            return UnaryExpr(op, right)

        return self.parse_primary()

    def parse_primary(self) -> Expr:
        if self.state.match_type(TokenType.FALSE):
            return LiteralExpr(False)

        if self.state.match_type(TokenType.TRUE):
            return LiteralExpr(True)

        if self.state.match_type(TokenType.NIL):
            return LiteralExpr(None)

        if self.state.match_type(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.state.previous().literal)

        if self.state.match_type(TokenType.LEFT_PAREN):
            expr = self.parse_expr()
            self.state.match_or_throw(
                TokenType.RIGHT_PAREN, "Missing closing parenthesis"
            )
            return GroupingExpr(expr)
        
        if self.state.match_type(TokenType.IDENT):
            return VariableExpr(self.state.previous())

        raise self.state.error(self.state.peek(), "Expected expression")

    
