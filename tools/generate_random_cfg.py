import random

MAX_DEPTH = 7
depth = 0

def expression():
    global depth
    depth += 1
    if depth >= MAX_DEPTH:
        return literal()
    
    if depth <= 2:
         nt = random.choice([unary, binary, grouping])
    else:
        nt = random.choice([literal, unary, binary, grouping])
    return nt()

def literal():
    return random.choice([
        str(random.randint(0, 100)),
        random.choice(['"foo"', '"bar"', '"boofar"', '"farboo"']),
        "true", "false", "nil"
    ])

def grouping():
    return "(" + expression() + ")"

def unary():
    return random.choice(["_", "!"]) + expression()

def binary():
    return expression() + operator() + expression()

def operator():
    return random.choice([
        "==", "!=", "<=", "<=", ">=", ">", "+", "-", "*", "/"
    ])

for i in range(10):
    print(expression())
    depth = 0

