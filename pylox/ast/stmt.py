from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pylox.token import Token
from pylox.ast.expr import Expr


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass

@dataclass
class PrintStmt(Stmt):
    expr: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_print_stmt(self)

@dataclass
class ExpressionStmt(Stmt):
    expr: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_expression_stmt(self)

@dataclass
class VarStmt(Stmt):
    name: Token
    initializer: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_var_stmt(self)



class Visitor(ABC):
    @abstractmethod
    def visit_print_stmt(self, stmt: PrintStmt): ...

    @abstractmethod
    def visit_expression_stmt(self, stmt: ExpressionStmt): ...

    @abstractmethod
    def visit_var_stmt(self, stmt: VarStmt): ...


