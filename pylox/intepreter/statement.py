from dataclasses import dataclass
from pylox.ast.stmt import ExpressionStmt, PrintStmt, Stmt, VarStmt, Visitor
from pylox.intepreter.expression import ExprEvaluator
from pylox.intepreter.utils import stringify
from pylox.intepreter.environment import Environment

@dataclass
class StmtEvaluator(Visitor):
    expr_evaluator: ExprEvaluator
    env: Environment
    
    def visit_print_stmt(self, stmt: PrintStmt):
        result = self.expr_evaluator.evaluate(stmt.expr)
        print(stringify(result))

    def visit_expression_stmt(self, stmt: ExpressionStmt):
        self.expr_evaluator.evaluate(stmt.expr)

    def visit_var_stmt(self, stmt: VarStmt):
        value = self.expr_evaluator.evaluate(stmt.initializer)
        self.env.define(stmt.name, value)

    def evaluate(self, stmt: Stmt):
        return stmt.accept(self)
    