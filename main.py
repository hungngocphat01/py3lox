from pylox import Intepreter
from pylox.ast.ast_printer import AstPrinter

source = """
var a = 1;
var b = 9.15;

a = 5*b/(1/8.23+2-(8/7*(2/3)));
print a;
print a > "n";
"""

Intepreter().intepret(source)
