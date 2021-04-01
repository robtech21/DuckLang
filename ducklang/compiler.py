from duck_parser import *
from duck_ast import *

import sys


class Compiler:
    def __init__(self, ast, vm):
        self.ast = ast
        self.vm = vm

        self.code = []
        self.constant_table = []

        self.locals = {}

    def compile(self, main_ast=None):
        if main_ast is None:
            main_ast = self.ast

        self.constant_table = []
        

        for ast in main_ast:
            if isinstance(ast, FunctionCall):
                if ast.name == "quack":
                    for argument in ast.arguments:
                        self.compile([argument])

                    self.code.append(("PRINT_VALUE", 0))

                elif ast.name == "swallow":
                    for argument in ast.arguments:
                        self.compile([argument])

                    self.code.append(("READ_INPUT", 0))

            elif isinstance(ast, Expr):
                self.constant_table.append(ast.value)
                index = self.constant_table.index(ast.value)

                self.code.append(("LOAD_VALUE", index))

            elif isinstance(ast, BinOp):
                self.constant_table.append(ast.rhs.value)

                index = self.constant_table.index(ast.rhs.value)
                self.code.append(("LOAD_VALUE", index))

                self.constant_table.append(ast.lhs.value)
                index = self.constant_table.index(ast.lhs.value)
                self.code.append(("LOAD_VALUE", index))

                if ast.op == "+":
                    self.code.append(("ADD_TWO_VALUES", 0))
                elif ast.op == "-":
                    self.code.append(("SUB_TWO_VALUES", 0))
                if ast.op == "*":
                    self.code.append(("MUL_TWO_VALUES", 0))
                elif ast.op == "/":
                    self.code.append(("DIV_TWO_VALUES", 0))

            elif isinstance(ast, AssignmentExpr):
                self.compile([ast.value])

                index = len(self.vm.stack) + 1

                self.locals[ast.name] = index

                self.code.append(("SET_LOCAL", index))

            elif isinstance(ast, VariableExpr):
                try:
                    depth = self.locals[ast.name]
                except KeyError:
                    sys.stderr.write(
                        f"Investigator Duck was looking for a variable, instead recieved {ast.name}")
                    sys.exit(1)

                self.code.append(("GET_LOCAL", depth))
        return self.code, self.constant_table