from typing import Any, List, Tuple

# zero argument functions (zeroArgFunction, tuple())
# one argument functions (oneArgFunc, (arg1,))
# three arg functions (threeArgFunc, (arg1, arg2, arg3))
# nested program (toplayerfunc, ((innerlayerfunc, (iarg1,)), arg2)


class Program:
    func: callable
    args: Tuple

    def __init__(self, func: callable, args: Tuple):
        if not callable(func) or type(args) is not tuple:
            raise TypeError("func must be a callable, and args must be a tuple")

        self.func = func
        self.args = args


def interpret(prog: Program) -> Any:
    calculated_args: list = []
    for a in prog.args:
        if type(a) is not Program:  # kinda like base case
            calculated_args.append(a)
        else:  # argument is a Program
            calculated_args.append(interpret(a))

    return prog.func(*calculated_args)