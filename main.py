from pylox.intepreter.interpreter import Intepreter

intepreter = Intepreter()
for lit in [1, 12.23, "true", "false", "nil", '"abcdef"']:
    result = intepreter.intepret("{0} == {0}".format(lit))
    print(result)