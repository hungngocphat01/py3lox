from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pylox.token import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass

@dataclass
class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_binary_expr(self)

@dataclass
class GroupingExpr(Expr):
    expr: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_grouping_expr(self)

@dataclass
class LiteralExpr(Expr):
    value: object

    def accept(self, visitor: Visitor):
        return visitor.visit_literal_expr(self)

@dataclass
class UnaryExpr(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_unary_expr(self)

@dataclass
class VariableExpr(Expr):
    name: Token

    def accept(self, visitor: Visitor):
        return visitor.visit_variable_expr(self)

@dataclass
class AssignmentExpr(Expr):
    name: Token
    value: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_assignment_expr(self)



class Visitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: BinaryExpr): ...

    @abstractmethod
    def visit_grouping_expr(self, expr: GroupingExpr): ...

    @abstractmethod
    def visit_literal_expr(self, expr: LiteralExpr): ...

    @abstractmethod
    def visit_unary_expr(self, expr: UnaryExpr): ...

    @abstractmethod
    def visit_variable_expr(self, expr: VariableExpr): ...

    @abstractmethod
    def visit_assignment_expr(self, expr: AssignmentExpr): ...


