# pylint: disable=W0123
import unittest
from pylox.intepreter import Intepreter
from pylox.intepreter.exc import IntepreterRuntimeError

class TestIntepreterExpr(unittest.TestCase):
    intepreter: Intepreter()

    def setUp(self) -> None:
        self.intepreter = Intepreter()
    
    def test_eq(self):
        for lit in [1, 12.23, "true", "false", "nil", '"abcdef"']:
            result = self.intepreter.intepret("{0} == {0}".format(lit))
            self.assertTrue(result)

    def intepret(self, s: str):
        return self.intepreter.intepret(s)

    def test_neq(self):
        self.assertFalse(self.intepret("1 != 1"))
        self.assertTrue(self.intepret("1 != 2"))
        self.assertTrue(self.intepret('"efgh" != "abcd"'))
        self.assertTrue(self.intepret("true != false"))

    def test_add_match(self):
        self.assertEqual(self.intepret("1.5 + 2"), 3.5)
        self.assertEqual(self.intepret('"abcd" + "efgh"'), "abcdefgh")
    
    def test_add_no_match(self):
        self.assertRaises(IntepreterRuntimeError, self.intepret, '123 + "abc"')
        self.assertRaises(IntepreterRuntimeError, self.intepret, '"def" + 45.67')

    def test_comp(self):
        self.assertFalse(self.intepret("1 >= 2"))
        self.assertFalse(self.intepret("100 < 1"))
        self.assertRaises(IntepreterRuntimeError, self.intepret, '"def" > 45.67')

    def test_complex1(self):
        expr = "(-1.123 * 2.1234) + 3.765 / -2.897"
        self.assertEqual(self.intepret(expr), eval(expr))

    def test_complex2(self):
        expr = "123 + 456 == 789"
        self.assertEqual(self.intepret(expr), eval(expr))

    def test_complex3(self):
        expr = '"abc" + "def" != "abcdef"'
        self.assertEqual(self.intepret(expr), eval(expr))

    def test_complex4(self):
        expr = '(1*3)-(9.75/678)*2/8+0.34-(3/(4+7/(9.34))) <= 4'
        self.assertEqual(self.intepret(expr), eval(expr))

if __name__ == "__main__":
    unittest.main()
