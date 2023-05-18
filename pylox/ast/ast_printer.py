import pylox.ast.expr as Expr
from pylox.ast.expr import AssignmentExpr, Visitor, BinaryExpr, GroupingExpr, LiteralExpr, VariableExpr, UnaryExpr

class AstPrinter(Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)
    
    def visit_binary_expr(self, expr: BinaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visit_grouping_expr(self, expr: GroupingExpr) -> str:
        return self.parenthesize("group", expr.expr)
    
    def visit_literal_expr(self, expr: LiteralExpr) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)
    
    def visit_unary_expr(self, expr: UnaryExpr):
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def visit_variable_expr(self, expr: VariableExpr):
        return self.parenthesize("var_ref", expr.name)

    def visit_assignment_expr(self, expr: AssignmentExpr):
        return self.parenthesize("var_asgn", expr.name, self.parenthesize(expr.value))

    def parenthesize(self, name: str, *args: Expr) -> str:
        s = "(" + name 
        for expr in args:
            s += " "
            s += expr.accept(self)
        s += ")"

        return s
