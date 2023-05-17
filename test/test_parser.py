import unittest

from typing import List
from pylox.parser.parser import Parser
from pylox.error_reporter import ErrorReporter
from pylox.ast import expr
from pylox.ast.ast_printer import AstPrinter
from pylox.token import TokenType, Token
from pylox.lexer.scanner import Scanner


def make_operator(t: TokenType, token: str):
    return Token(t, token, None, 1)

def lex(s: str):
    lexer = Scanner(s, ErrorReporter())
    return lexer.scan_tokens()

def parse(tokens: List[Token]):
    e = ErrorReporter()
    parser = Parser(tokens, e)

    return parser.parse(), e

def stringify(ast: expr.Expr):
    printer = AstPrinter()
    return printer.print(ast)


class TestSingleParser(unittest.TestCase):
    def test_binary(self):
        operators = [
            make_operator(t, token)
            for t, token in [
                (TokenType.PLUS, "+"),
                (TokenType.MINUS, "-"),
                (TokenType.STAR, "*"),
                (TokenType.SLASH, "/"),
                (TokenType.EQ_EQ, "=="),
                (TokenType.BANG_EQ, "!="),
                (TokenType.LESS_EQ, "<="),
                (TokenType.GREATER, ">"),
            ]
        ]

        for operator in operators:
            tokens = [
                Token(TokenType.NUMBER, "12.34", 12.34, 1),
                operator,
                Token(TokenType.STRING, '"abcdef"', "abcdef", 1),
                Token(TokenType.EOF, None, None, 1),
            ]

            ast, e = parse(tokens)

            self.assertFalse(e.had_error)
            self.assertIsInstance(ast, expr.Binary)
            self.assertEqual(ast.operator.lexeme, operator.lexeme)
            self.assertEqual(getattr(ast.left, "value"), 12.34)
            self.assertEqual(getattr(ast.right, "value"), "abcdef")

    def test_unary(self):
        operators = [
            make_operator(t, token)
            for t, token in [
                (TokenType.BANG, "!"),
                (TokenType.MINUS, "-"),
            ]
        ]

        for operator in operators:
            tokens = [
                operator,
                Token(TokenType.STRING, '"abcdef"', "abcdef", 1),
                Token(TokenType.EOF, None, None, 1),
            ]

            ast, e = parse(tokens)

            self.assertFalse(e.had_error)
            self.assertIsInstance(ast, expr.Unary)
            self.assertEqual(ast.operator.lexeme, operator.lexeme)
            self.assertEqual(getattr(ast.right, "value"), "abcdef")

    def test_grouping(self):
        tokens = [
            Token(TokenType.LEFT_PAREN, '(', None, 1),
            Token(TokenType.NUMBER, '12', 12, 1),
            Token(TokenType.RIGHT_PAREN, ')', None, 1),
            Token(TokenType.EOF, None, None, 1),
        ]

        ast, e = parse(tokens)

        self.assertFalse(e.had_error)
        self.assertIsInstance(ast, expr.Grouping)
        self.assertEqual(ast.expr, expr.Literal(12))

    def test_grouping_throw(self):
        tokens = [
            Token(TokenType.LEFT_PAREN, '(', None, 1),
            Token(TokenType.NUMBER, '12', 12, 1),
            Token(TokenType.EOF, None, None, 1),
        ]

        _, e = parse(tokens)
        self.assertTrue(e.had_error)


class TestPrecedence(unittest.TestCase):
    # This test assumes that the lexer works
    def test1(self):
        tokens = lex('("abcd" == 12) > 5 +7')
        ast, e = parse(tokens)

        self.assertFalse(e.had_error)
        s = stringify(ast)

        self.assertEqual(s, '(> (group (== abcd 12.0)) (+ 5.0 7.0))')

    def test2(self):
        tokens = lex('!5>= (1 !=5 * 4+- 2)')
        ast, e = parse(tokens)

        self.assertFalse(e.had_error)
        s = stringify(ast)

        self.assertEqual(s, '(>= (! 5.0) (group (!= 1.0 (+ (* 5.0 4.0) (- 2.0)))))')

    def test3(self):
        tokens = lex('1 == 2 >= 5 != 6')
        ast, e = parse(tokens)

        self.assertFalse(e.had_error)
        s = stringify(ast)

        self.assertEqual(s, '(!= (== 1.0 (>= 2.0 5.0)) 6.0)')

if __name__ == "__main__":
    unittest.main()
