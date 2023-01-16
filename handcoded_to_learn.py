import primitives as prim
# todo maybe do from prmitives import *

# Goal
"""
num2 must be positive
"""
def positive_plus(num1: int, num2: int):
    return prim.ind(num1, num2, prim.succ)

# def greater_than()
# def neg(num):
#     return prim.ind(num, positive_plus(num, num), prim.pred)


# works for both positive and negative numbers
def plus(num1: int, num2: int):
    return prim.ind(num1,
             prim.cond(
                 prim.less_than(prim.zero(), num2),
                 num2,  # num2 positive case
                 prim.neg(num2)  # num2 negative case
             ),
             prim.cond(
                 prim.less_than(prim.zero(), num2),
                 prim.succ,  # num2 positive case
                 prim.pred  # num2 negative case
             )
    )
    # prim.cond(prim.less_than(prim.zero(), num2),
    #     # num2 positive case
    #     positive_plus(num1, num2),
    #
    #     # num2 negative case
    #     prim.ind(num1, neg(num2), prim.pred)  # todo maybe make this to a positive minus
    # )






# greater than
#
# how to learn plus
# - multiplication
#     - doubling
#     - triple
#     - quadruple
#     - quintiple
# - plus-y divisible by
# - within 5 of
# - sum
# - increment by 10
#
# 5*8
# ((5+5)*2) vs. 5+5+5+5+5+5+5
# you can use bits and stuff...
#
#
#
#
# substraction (repeated predecesor)
# - isdivisible by
#     - divide
# -

