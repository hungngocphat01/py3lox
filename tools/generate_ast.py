expr = {
    "Binary": ("left: Expr", "operator: Token", "right: Expr"),
    "Grouping": ("expr: Expr",),
    "Literal": ("value: object",),
    "Unary": ("operator: Token", "right: Expr")
}


def generate_ast():
    out_content = "\n".join((
        "from __future__ import annotations",
        "from abc import ABC, abstractmethod",
        "from dataclasses import dataclass",
        "from pylox.token import Token",
        "",
        "",
        "class Expr(ABC):",
        "    @abstractmethod",
        "    def accept(self, visitor: Visitor):",
        "        pass"
    ))

    for class_name, fields in expr.items():
        class_def = ("\n\n@dataclass\n"
                    f"class {class_name}(Expr):")
        for field in fields:
            class_def += "\n    " + field

        # define visit function
        visit_func = "\n".join((
            "\n",
            "    def accept(self, visitor: Visitor):",
            f"        return visitor.visit_{class_name.lower()}_expr(self)"
        ))
        class_def += visit_func

        out_content += class_def
    
    return out_content

def generate_visitors():
    out_content = "\n".join((
        "", "",
        "class Visitor(ABC):\n",
    ))

    for class_name in expr:
        visitor_method = "\n".join((
            "    @abstractmethod",
            f"    def visit_{class_name.lower()}_expr(self, expr: {class_name}): ...",
            "\n"
        ))

        out_content += visitor_method
    
    return out_content

if __name__ == "__main__":
    print(generate_ast())
    print()
    print(generate_visitors())
    