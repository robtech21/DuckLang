import compiler, duck_parser, vm


def repl():
    """
    This function defines the debugging monkelang REPL environment. It runs 
    code with the VM class's run_once method.
    """
    machine = vm.VM([])
    duck_compiler = compiler.Compiler([], machine)

    print("DuckLang REPL :D")

    while True:
        command = input("duck> ")

        ast = duck_parser.DuckParser(command).parse()

        duck_compiler.ast = ast

        code, constant_table = duck_compiler.compile()
        
        machine.constant_table = constant_table
        machine.code = code

        machine.run_once(code)


repl()
