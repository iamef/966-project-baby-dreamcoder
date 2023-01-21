from typing import Any, List, Tuple

# zero argument functions (zeroArgFunction, tuple())
# one argument functions (oneArgFunc, (arg1,))
# three arg functions (threeArgFunc, (arg1, arg2, arg3))
# nested program (toplayerfunc, ((innerlayerfunc, (iarg1,)), arg2)
def interpret(program: Tuple[callable, Tuple]) -> Any:
    func, args = program

    calculated_args: list = []
    for a in args:
        if type(a) is not tuple:
            calculated_args.append(a)
        else:
            if callable(a[0]):
                calculated_args.append(interpret(a))

    return func(*calculated_args)