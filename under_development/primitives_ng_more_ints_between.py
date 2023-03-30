from primitives_ng_more_ints import *

# TODO update prim_weights to account for bool: (int, int, int) case

def is_between(inp: int, num1: int, num2: int) -> bool:
    return num1 < inp and inp < num2
