from typing import Type
from dataclasses import dataclass
from pylox.token import TokenType, Token
from pylox.ast.expr import (
    AssignmentExpr,
    BinaryExpr,
    GroupingExpr,
    LiteralExpr,
    UnaryExpr,
    VariableExpr,
    Visitor,
    Expr,
)
from pylox.intepreter.exc import IntepreterRuntimeError
from pylox.intepreter.environment import Environment


@dataclass
class ExprEvaluator(Visitor):
    env: Environment

    def visit_literal_expr(self, expr: LiteralExpr) -> object:
        return expr.value

    def visit_grouping_expr(self, expr: GroupingExpr) -> object:
        return self.evaluate(expr.expr)

    def visit_unary_expr(self, expr: UnaryExpr):
        right = self.evaluate(expr.right)

        match (expr.operator.token_type):
            case TokenType.MINUS:
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy(right)

    def visit_binary_expr(self, expr: BinaryExpr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        result = None

        match (expr.operator.token_type):
            case TokenType.PLUS:
                if not (
                    self.are_same_type(str, left, right)
                    or self.are_same_type(float, left, right)
                ):
                    raise IntepreterRuntimeError(
                        expr.operator, "Operands should be two numbers or two strings"
                    )
                result = left + right
            case TokenType.MINUS:
                self.ensure_numbers(expr.operator, left, right)
                result = left - right
            case TokenType.STAR:
                self.ensure_numbers(expr.operator, left, right)
                result = left * right
            case TokenType.SLASH:
                self.ensure_numbers(expr.operator, left, right)
                result = left / right
            case TokenType.GREATER:
                self.ensure_numbers(expr.operator, left, right)
                result = left > right
            case TokenType.LESS:
                self.ensure_numbers(expr.operator, left, right)
                result = left < right
                self.ensure_numbers(expr.operator, left, right)
            case TokenType.GREATER_EQ:
                result = left >= right
                self.ensure_numbers(expr.operator, left, right)
            case TokenType.LESS_EQ:
                self.ensure_numbers(expr.operator, left, right)
                result = left < right
            case TokenType.BANG_EQ:
                result = left != right
            case TokenType.EQ_EQ:
                result = left == right

        return result

    def visit_variable_expr(self, expr: VariableExpr):
        return self.env.get(expr.name)

    def visit_assignment_expr(self, expr: AssignmentExpr):
        value = self.evaluate(expr.value)
        self.env.assign(expr.name, value)

    def ensure_numbers(self, operator: Token, *args: object):
        if not self.are_same_type(float, *args):
            raise IntepreterRuntimeError(operator, "Operands must be numbers")

    def are_same_type(self, t: Type, *args: object):
        return all(isinstance(arg, t) for arg in args)

    def is_truthy(self, value: object) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return bool(value)
        if value is None:
            return False

        return True

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)
