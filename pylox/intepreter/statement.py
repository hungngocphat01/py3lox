from typing import Type
from dataclasses import dataclass
from pylox.token import TokenType, Token
from pylox.ast.expr import Expr
from pylox.ast.stmt import ExpressionStmt, PrintStmt, Stmt, Visitor
from pylox.intepreter.exc import IntepreterRuntimeError
from pylox.intepreter.expression import ExprEvaluator
from pylox.intepreter.utils import stringify

@dataclass
class StmtEvaluator(Visitor):
    expr_evaluator: ExprEvaluator
    
    def visit_print_stmt(self, stmt: PrintStmt):
        result = self.expr_evaluator.evaluate(stmt.expr)
        print(stringify(result))

    def visit_expression_stmt(self, stmt: ExpressionStmt):
        self.expr_evaluator.evaluate(stmt.expr)

    def evaluate(self, stmt: Stmt):
        return stmt.accept(self)
    