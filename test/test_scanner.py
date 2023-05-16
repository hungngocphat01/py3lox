import unittest
from pylox.lexer.scanner import Scanner, ONE_CHAR_TOKENS, CONDITIONAL_TOKENS
from pylox.error_reporter import ErrorReporter
from pylox.token import TokenType

class TestLexOperators(unittest.TestCase):
    def test_one_char(self):
        for char, expected_type in ONE_CHAR_TOKENS.items():
            scanner = Scanner(char, ErrorReporter())
            tokens = scanner.scan_tokens()

            self.assertEqual(tokens[0].lexeme, char)
            self.assertEqual(tokens[0].token_type, expected_type)

    def test_two_char_single(self):
        for char, char_entry in CONDITIONAL_TOKENS.items():
            scanner = Scanner(char, ErrorReporter())
            tokens = scanner.scan_tokens()
            self.assertEqual(tokens[0].token_type, char_entry[0])

    def test_two_char_composite(self):
        for char, char_entry in CONDITIONAL_TOKENS.items():
            composite_char = char + char_entry[1][0]
            scanner = Scanner(composite_char, ErrorReporter())
            tokens = scanner.scan_tokens()
            self.assertEqual(tokens[0].token_type, char_entry[1][1])

    def test_grouping(self):
        scanner = Scanner("(( )){}", ErrorReporter())
        tokens = scanner.scan_tokens()
        raw_tokens = [t.lexeme for t in tokens]
        self.assertListEqual(raw_tokens, ["(", "(", ")", ")", "{", "}", ""])

    def test_comment(self):
        scanner = Scanner("() + // parentheses", ErrorReporter())
        tokens = scanner.scan_tokens()
        raw_tokens = [t.lexeme for t in tokens]
        self.assertListEqual(raw_tokens, ["(", ")", "+", ""])

    def test_all_operators(self):
        scanner = Scanner("!*-+/=<> <= ==", ErrorReporter())
        tokens = scanner.scan_tokens()
        raw_tokens = [t.lexeme for t in tokens]
        self.assertListEqual(raw_tokens, 
                             ["!", "*", "-", "+", "/", "=", "<", ">", "<=", "==", ""])

class TestLiterals(unittest.TestCase):
    def test_string_literal(self):
        scanner = Scanner('"this is a string"', ErrorReporter())
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].literal, "this is a string")

    def test_string_not_terminated(self):
        reporter = ErrorReporter()
        scanner = Scanner('"should thow', reporter)
        scanner.scan_tokens()
        self.assertTrue(reporter.had_error)
    
    def test_integer(self):
        scanner = Scanner("123", ErrorReporter())
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].literal, 123.0)
    
    def test_float(self):
        scanner = Scanner("123.456", ErrorReporter())
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].literal, 123.456)

class TestStatements(unittest.TestCase):
    def test_declare(self):
        scanner = Scanner("var a = 1.56", ErrorReporter())
        tokens = scanner.scan_tokens()

        expect = [
            ("var", TokenType.VAR),
            ("a", TokenType.IDENT),
            ("=", TokenType.EQ),
            ("1.56", TokenType.NUMBER),
            ("", TokenType.EOF)
        ]

        for ex, tok in zip(expect, tokens):
            self.assertEqual(ex[0], tok.lexeme)
            self.assertEqual(ex[1], tok.token_type)

    def test_if(self):
        scanner = Scanner("""
            if (a <= 6) {
                var b = 7;
            }
        """, ErrorReporter())

        tokens = scanner.scan_tokens()

        expect = [
            ("if", TokenType.IF),
            ("(", TokenType.LEFT_PAREN),
            ("a", TokenType.IDENT),
            ("<=", TokenType.LESS_EQ),
            ("6", TokenType.NUMBER),
            (")", TokenType.RIGHT_PAREN),
            ("{", TokenType.LEFT_BRACE),
            ("var", TokenType.VAR),
            ("b", TokenType.IDENT),
            ("=", TokenType.EQ),
            ("7", TokenType.NUMBER),
            (";", TokenType.SEMICOLON),
            ("}", TokenType.RIGHT_BRACE),
            ("", TokenType.EOF)
        ]

        for ex, tok in zip(expect, tokens):
            self.assertEqual(ex[0], tok.lexeme)
            self.assertEqual(ex[1], tok.token_type)


if __name__ == "__main__":
    unittest.main()
