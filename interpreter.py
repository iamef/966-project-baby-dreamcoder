from typing import Any, List, Tuple

# try the head args form
def interpret(program: Tuple[callable, Tuple]):
    if len(program) == 0:
        return
    elif not callable(program[0]):
        return program
    return program[0](*interpret(program[1]))
