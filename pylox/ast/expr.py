from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pylox.token import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visitBinaryExpr(self)

@dataclass
class Grouping(Expr):
    expr: Expr

    def accept(self, visitor: Visitor):
        return visitor.visitGroupingExpr(self)

@dataclass
class Literal(Expr):
    value: object

    def accept(self, visitor: Visitor):
        return visitor.visitLiteralExpr(self)

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visitUnaryExpr(self)



class Visitor(ABC):
    @abstractmethod
    def visitBinaryExpr(self, expr: Binary): ...

    @abstractmethod
    def visitGroupingExpr(self, expr: Grouping): ...

    @abstractmethod
    def visitLiteralExpr(self, expr: Literal): ...

    @abstractmethod
    def visitUnaryExpr(self, expr: Unary): ...


