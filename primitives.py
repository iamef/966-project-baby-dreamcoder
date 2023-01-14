
# number manipulations
def zero():
    return 0


def pred(num: int):
    return num - 1


def succ(num: int):
    return num + 1


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
    # see if our program is good enough to deal with this
    if bool_item:
        return if_item
    return else_item


# ind stands for induction
def ind(input1, num_times: int, f):
    return cond(
        eq(num_times, 0),
        input1,
        ind(f(input1), pred(num_times), f)
    )




# ind(b)(h)(succ(n)) =
# ind(b)(h)(0) = h(ind(b)(b))


# list manipulations
def first(l: list):
    return l[0]


def last(l: list):
    return l[-1]



