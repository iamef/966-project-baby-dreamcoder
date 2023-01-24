from typing import Any

# number manipulations
# alternatively we could just have integers in general be primitives

def zero() -> int:
    return 0


def pred(num: int) -> int:
    return num - 1


def succ(num: int) -> int:
    return num + 1


def neg(num: int) -> int:
    return -1 * num


def eq(num1: int, num2: int) -> bool:
    return num1 == num2


def less_than(num1: int, num2: int) -> bool:
    return num1 < num2


# boolean things
def conj(bool1: bool, bool2: bool) -> bool:
    # and (conjunction)
    return bool1 and bool2


def disj(bool1: bool, bool2: bool) -> bool:
    # or (disjunction)
    return bool1 or bool2


def cond(bool_item: bool, if_item: Any, else_item: Any) -> Any:
    # note that else_item may be None
    # note that both the if_item and else_item are run and evaluated
    #      before enterring this function
    if bool_item:
        return if_item
    return else_item


# recursion
def ind(input1: Any, num_times: int, f: callable) -> Any:
    # ind stands for induction

    # can't use cond here because it will run ind even if num_times is 0
    if less_than(num_times, zero()):
        raise ValueError("num times cannot be negative")
    elif eq(num_times, zero()):
        return input1
    return ind(f(input1), pred(num_times), f)

# ind(b)(h)(succ(n)) =
# ind(b)(h)(0) = h(ind(b)(b))


# # list manipulations
# def first(l: list):
#     return l[0]
#
#
# def last(l: list):
#     return l[-1]

