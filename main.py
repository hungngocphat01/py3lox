from pylox import Intepreter

source = "print (1/2)*3+4;"

intepreter = Intepreter()
result = intepreter.intepret("""
var a = 1;
var b = 2;
print a+b;
""")
