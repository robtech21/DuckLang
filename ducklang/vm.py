from inspect import signature
import sys


class VM:
    def __init__(self, code):
        self.code = code

        self.stack = []
        self.constant_table = []

        self.pc = 0

    def LOAD_VALUE(self, argument):
        value = self.constant_table[argument]
        self.stack.append(value)
        self.pc += 1

    def PRINT_VALUE(self):
        value = self.stack.pop()
        print(value)
        self.pc += 1
    
    def READ_INPUT(self):
        value = self.stack.pop()
        data = input(value)
        self.stack.append(data)
        self.pc += 1

    def ADD_TWO_VALUES(self):
        lhs = self.stack.pop()
        rhs = self.stack.pop()

        self.stack.append(lhs + rhs)
        self.pc += 1

    def SUB_TWO_VALUES(self):
        lhs = self.stack.pop()
        rhs = self.stack.pop()

        self.stack.append(lhs - rhs)
        self.pc += 1

    def MUL_TWO_VALUES(self):
        lhs = self.stack.pop()
        rhs = self.stack.pop()

        self.stack.append(lhs * rhs)
        self.pc += 1

    def DIV_TWO_VALUES(self):
        lhs = self.stack.pop()
        rhs = self.stack.pop()

        self.stack.append(lhs / rhs)
        self.pc += 1

    def SET_LOCAL(self, argument):
        value = self.stack[-1]
        self.stack.insert(argument, value)
        self.pc +=1

    def GET_LOCAL(self, argument):
        value = self.stack[argument]
        self.stack.append(value)
        self.pc += 1

    def run(self):
        while True:
            if self.pc > len(self.code):
                sys.exit(0)

            instruction = self.code[self.pc]
            function = getattr(self, instruction[0])

            sig = signature(function)

            if len(sig.parameters) == 1:
                function(instruction[1])
            else:
                instruction()

    def run_once(self, code):
        while True:
            if self.pc >= len(code):
                break

            instruction = code[self.pc]

            function = getattr(self, instruction[0])

            sig = signature(function)

            if len(sig.parameters) == 1:
                function(instruction[1])
            else:
                function()
