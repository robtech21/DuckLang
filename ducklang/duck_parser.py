from duck_ast import *
import sys
from lexer import Lexer


class DuckParser:
    def __init__(self, string_input):
        self.string_input = string_input

        self.lexer = Lexer(string_input)
        self.lexer.lex()

    def parse(self):
        ast = []

        for token in self.lexer.tokens:
            current_token = self.lexer.next()

            if current_token.type == "QUACK":
                if self.lexer.peek().type == "LBRACE":
                    arguments = []
                    while current_token.type != "RBRACE":
                        current_token = self.lexer.next()

                        argument = self.parse_argument(current_token)
                        for arg in argument:
                            arguments.append(arg)
                else:
                    sys.stderr.write(
                        f"Coder Duck wanted '(', but instead found {self.lexer.peek().text}")
                    sys.exit(1)

                quack = FunctionCall("quack", arguments)

                ast.append(quack)

            elif current_token.type == "SWALLOW":
                if self.lexer.peek().type == "LBRACE":
                    arguments = []
                    while current_token.type != "RBRACE":
                        current_token = self.lexer.next()

                        argument = self.parse_argument(current_token)

                        for arg in argument:
                            arguments.append(arg)
                else:
                    sys.stderr.write(
                        f"Coder Duck wanted 'quack', but instead found {self.lexer.peek().text}"
                    )
                    sys.exit()

                swallow = FunctionCall("swallow", arguments)

                ast.append(swallow)

            elif current_token.type == "IDENT":
                name = self.lexer.current_token.text

                next_token = self.lexer.peek()

                if next_token.type != "ASSIGNMENT":
                    variable = VariableExpr(name)

                    ast.append(variable)

                    continue

                equals = self.lexer.next()

                value = self.lexer.next()

                if value.type == "INTEGER":
                    value = Expr(int(value.text))
                elif value.type in ("DOUBLEQUOTEDSTRING", "SINGLEQUOTEDSTRING"):
                    value = Expr(str(value.text).replace(
                        '"', "").replace("'", ""))
                elif value.type == "SWALLOW":
                    arguments = []
                    while current_token.type != "RBRACE":
                        current_token = self.lexer.next()
                        argument = self.parse_argument(current_token)
                                                
                        for arg in argument:
                            arguments.append(arg)
                    value = FunctionCall('swallow', arguments)
                else:
                    sys.stderr.write(
                        f"Mr.Duck Quackington's newspaper had the wrong stuff; He had expected a STRING or an INTEGER, but found {value.type}: {value.text}"
                    )
                    sys.exit(1)

                assignment_expr = AssignmentExpr(name, value)

                ast.append(assignment_expr)

            elif self.lexer.current_token.type == "EOF":
                break
        return ast

    def parse_argument(self, current_token):
        arguments = []
        if current_token.type == "INTEGER":
            integer = Expr(int(current_token.text))

            arguments.append(integer)

        elif current_token.type in ("DOUBLEQUOTEDSTRING", "SINGLEQUOTEDSTRING"):
            string = Expr(str(current_token.text).replace(
                '"', "").replace("'", ""))

            arguments.append(string)

        elif current_token.type == "PLUS":
            lhs = self.lexer.tokens[self.lexer.token_pos - 1]

            arguments.pop()

            rhs = self.lexer.next()

            if lhs.type == "INTEGER":
                if rhs.type == "INTEGER":
                    binop = BinOp(
                        Expr(int(lhs.text)), Expr(int(rhs.text)), "+")

                    arguments.append(binop)
                elif rhs.type in ("DOUBLEQUOTEDSTRING", "SINGLEQUOTEDSTRING"):
                    sys.stderr.write(
                        f"Important: FDI (Federal Ducks Of Investigation) is at your door for making this mistake: You cannot add INTEGER {lhs.text} to STRING {rhs.text}")
                    sys.exit(1)
            elif lhs.type in ("DOUBLEQUOTEDSTRING", "SINGLEQUOTEDSTRING"):
                if rhs.type in ("DOUBLEQUOTEDSTRING", "SINGLEQUOTEDSTRING"):
                    binop = BinOp(Expr(str(lhs.text.replace('"', "").replace("'", ""))), Expr(
                        str(rhs.text).replace('"', "").replace("'", "")), "+")

                    arguments.append(binop)
                elif rhs.type == "INTEGER":
                    sys.stderr.write(
                        f"Ducky had another problem with his quacks: Ducky was helpless because he was unable to join STRING {lhs.text} with INTEGER {rhs.text}")
                    sys.exit(1)
        elif current_token.type == "MINUS":
            lhs = self.lexer.tokens[self.lexer.token_pos - 1]

            arguments.pop()

            rhs = self.lexer.next()

            if lhs.type == "INTEGER":
                if rhs.type == "INTEGER":
                    binop = BinOp(
                        Expr(int(lhs.text)), Expr(
                            int(rhs.text)), "-"
                    )

                    arguments.append(binop)
                elif rhs.type in ("DOUBLEQUOTEDSTRING", "SINGLEQUOTEDSTRING"):
                    sys.stderr.write(
                        f"Ducky stares at you as you to to subtract STRING {rhs.text} from INTEGER {lhs.text}")
                    sys.exit(1)
            elif lhs.type == "STRING":
                sys.stderr.write(
                    f"As a wise duck once said: You cannot subtract using STRING {lhs.text}")
                sys.exit(1)

        elif current_token.type == "STAR":
            lhs = self.lexer.tokens[self.lexer.token_pos - 1]

            arguments.pop()

            rhs = self.lexer.next()

            if lhs.type == "INTEGER":
                if rhs.type == "INTEGER":
                    binop = BinOp(
                        Expr(int(lhs.text)), Expr(
                            int(rhs.text)), "*"
                    )

                    arguments.append(binop)
                elif rhs.type in ("DOUBLEQUOTEDSTRING", "SINGLEQUOTEDSTRING"):
                    binop = BinOp(
                        Expr(int(lhs.text)), Expr(
                            str(rhs.text).replace('"', "").replace("'", "")), "*"
                    )

                    arguments.append(binop)
            elif lhs.type in ("DOUBLEQUOTEDSTRING", "SINGLEQUOTEDSTRING"):
                if rhs.type == "INTEGER":
                    binop = BinOp(
                        Expr(str(lhs.text.replace('"', "").replace("'", ""))), Expr(
                            int(rhs.text)), "*"
                    )

                    arguments.append(binop)
                elif rhs.type in ("DOUBLEQUOTEDSTRING", "SINGLEQUOTEDSTRING"):
                    sys.stderr.write(
                        f"Mr.Duck Duckington covers his eyes as you try to multiply STRING {lhs.text} by STRING {rhs.text}")
                    sys.exit(1)
        elif current_token.type == "SLASH":
            lhs = self.lexer.tokens[self.lexer.token_pos - 1]

            arguments.pop()

            rhs = self.lexer.next()

            if lhs.type == "INTEGER":
                if rhs.type == "INTEGER":
                    binop = BinOp(
                        Expr(int(lhs.text)), Expr(
                            int(rhs.text)), "/"
                    )

                    arguments.append(binop)
                elif rhs.type in ("DOUBLEQUOTEDSTRING", "SINGLEQUOTEDSTRING"):
                    sys.stderr.write(
                        f" Mr.Ducko the Mathematecian says: You cannot divide STRING {rhs.text} by INTEGER {lhs.text}")
                    sys.exit(1)
            elif lhs.type == "STRING":
                sys.stderr.write(
                    f"Please stop trying to divide using STRING {lhs.text}, All the ducklings are looking at you")
                sys.exit(1)
        elif current_token.type == "IDENT":
            name = self.lexer.current_token.text

            next_token = self.lexer.peek()

            if next_token.type == "ASSIGNMENT":
                sys.stderr.write(
                    "You're not allowed to assign variables inside a QUACK. Didn't Ms.Duck already tell you this.")
                sys.exit(1)

            else:
                variable = VariableExpr(name)

                arguments.append(variable)

        return arguments
