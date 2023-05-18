from pylox import Token
from pylox.intepreter.exc import IntepreterRuntimeError

class Environment:
    def __init__(self):
        self._env = {}
    
    def get(self, name: Token) -> object:
        value = self._env.get(name)
        if value is None:
            raise IntepreterRuntimeError(name, "Variable undefined: {}".format(name.lexeme))
        return value

    def define(self, name: Token, initializer: object):
        self._env[name] = initializer
        