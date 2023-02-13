from primitives_number_game import *

prim_weights = {
    int: {  # output is int
        tuple(): 1,
        (int,): 1/4,
        (int, int): 1,
        (bool, int, int): 1/3,
        (int, int, callable): 1/5  # doesn't exist in primitives number game
    },
    bool: {
        (int, int): 1,
        (bool, bool): 1
    },
    callable: {
        (bool, callable, callable): 1
    }
}

def two() -> int:
    return 2


def five() -> int:
    return 5


def ten() -> int:
    return 10


def twenty() -> int:
    return 20


def thirty() -> int:
    return 30


def forty() -> int:
    return 40


def fifty() -> int:
    return 50


def sixty() -> int:
    return 60


def seventy() -> int:
    return 70


def eighty() -> int:
    return 80


def ninety() -> int:
    return 90


def one_hundred() -> int:
    return 100
