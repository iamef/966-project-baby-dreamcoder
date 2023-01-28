from typing import Any, List, Tuple
import re

# zero argument functions (zeroArgFunction, tuple())
# one argument functions (oneArgFunc, (arg1,))
# three arg functions (threeArgFunc, (arg1, arg2, arg3))
# nested program (toplayerfunc, ((innerlayerfunc, (iarg1,)), arg2)


class Program:
    func: callable
    func_name: str
    args: Tuple

    def __init__(self, func: callable, args: Tuple):
        """

        :param func: note the x_number has to be a direct arg of a program or subprogram
                (can't be tucked into a tuple or list as of now)
        :param args: if the args are variables, they can be named "x_number"
        """
        if not callable(func) or type(args) is not tuple:
            raise TypeError("func must be a callable, and args must be a tuple")

        self.func = func
        self.func_name = func.__name__

        self.args = args


def interpret(prog: Program, inp=None) -> Any:
    """

    :param prog: note the x_number has to be a direct arg of a program or subprogram
                (can't be tucked into a tuple or list as of now)
    :param inp: used to fill in the "x_number" stuff...
    :return:
    """
    calculated_args: list = []
    for a in prog.args:
        if type(a) is not Program:  # kinda like base case
            # todo make this a little bit safer
            if type(a) is str and re.fullmatch("^x_(\\d+)$", "x_0"):
                inp_index = int(a.split("_")[1])
                calculated_args.append(inp[inp_index])
            else:
                calculated_args.append(a)
        else:  # argument is a Program
            calculated_args.append(interpret(a, inp))

    return prog.func(*calculated_args)

    # if program and input pairs, because there are a lot of
    # depth 1 inputs are the same
    # todo we can also incorporate some hashing