class FunctionCall:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class Expr:
    def __init__(self, value):
        self.value = value


class BinOp:
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op


class AssignmentExpr:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class VariableExpr:
    def __init__(self, name):
        self.name = name