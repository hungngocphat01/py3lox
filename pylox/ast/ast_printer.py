import pylox.ast.expr as Expr
from pylox.ast.expr import Visitor, Binary, Grouping, Literal, Unary

class AstPrinter(Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)
    
    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visitGroupingExpr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expr)
    
    def visitLiteralExpr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)
    
    def visitUnaryExpr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *args: Expr) -> str:
        s = "(" + name 
        for expr in args:
            s += " "
            s += expr.accept(self)
        s += ")"

        return s
