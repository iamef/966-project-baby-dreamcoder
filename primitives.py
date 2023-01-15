
# number manipulations
# alternatively we could just have integers in general be primitives
def zero():
    return 0


def pred(num: int):
    return num - 1


def succ(num: int):
    return num + 1

def neg(num: int):
    return -1 * num


def eq(num1: int, num2: int):
    return num1 == num2


def less_than(num1: int, num2: int):
    return num1 < num2


# boolean things
def conj(bool1, bool2):
    # and (conjunction)
    return bool1 and bool2


def disj(bool1, bool2):
    # or (disjunction)
    return bool1 or bool2


def cond(bool_item, if_item, else_item):
    # note that else_item may be None
    # note that both the if_item and else_item are run and evaluated
    #      before enterring this function
    if bool_item:
        return if_item
    return else_item


# recursion
def ind(input1, num_times: int, f):
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