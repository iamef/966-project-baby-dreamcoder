import primitives as prim

import inspect
from typing import Tuple, List, Any, Callable
from problem import Problem

from interpreter import *


def has_input_type(input_type: Tuple[type, ...], f: callable):
    if input_type is None:
        return True

    f_argsspec = inspect.getfullargspec(f)

    f_args = f_argsspec.args

    # a dictionary mapping variable names to types
    f_args_annotations = f_argsspec.annotations

    if len(f_args) == 0:
        return True

    for arg in f_args:
        if f_args_annotations[arg] is Any:
            return True
        elif f_args_annotations[arg] in input_type:
            return True

    return False

    type_overlap = set(f_args_annotations.values()).intersection(set(input_type).union({Any}))
    # reminder to add the any type

    return len(type_overlap) > 0


def has_output_type(output_type: type, f: callable):
    # todo figure this part out
    # return True

    # a dictionary mapping variable names to types
    f_args_annotations = inspect.getfullargspec(f).annotations
    return f_args_annotations['return'] is Any or f_args_annotations['return'] is output_type
    # f_return_annotation = inspect.signature(prim.zero).return_annotation
    #
    # type_overlap = set(f_return_annotation).intersection(set(output_type).union({Any}))
    #
    # return len(type_overlap) > 0


def get_functions_filtered(filt: Callable[[Tuple[Callable, str]], bool]) -> List[Tuple[str, callable]]:
    """

    :param filt: callable. input is a Tuple (function_name: string, function: callable)
                            output is a boolean indicating whether or not the function passes the filter or not
    :return: a list of functions in List[Tuple]
    TODO double check on the thing it actually returns.
    """
    funcs = inspect.getmembers(prim, lambda f: inspect.isfunction(f) and filt(f))

    # sort functions by number of arguments, then by name
    # todo in the future sort the functions by Bayesian probabilities
    funcs.sort(key=lambda f: (f[1].__code__.co_argcount, f[0]))

    return funcs


def get_functions_by_types(input_type: Tuple[type, ...], output_type: type) -> List[Tuple[str, callable]]:
    """
    gets function with at least one of the input types

    if input_type is None, rather than (None,), we ignore input_type
    similarly if output_type is None, rather than NoneType, we ignore output_type


    returns function in order of least number of inputs to most number of inputs
    """
    def is_right_type(f):
        # todo the is function is not necessary
        return inspect.isfunction(f) and has_input_type(input_type, f) and has_output_type(output_type, f)

    return get_functions_filtered(is_right_type)


def get_functions_by_output_type(output_type: type) -> List[Tuple[str, callable]]:
    return get_functions_filtered(
        # todo the is function is not necessary
        lambda f: inspect.isfunction(f) and has_output_type(output_type, f)
    )



def get_functions_by_output_type(output_type: type) -> List[callable]:
    funcs = inspect.getmembers(
        prim,
        lambda f: inspect.isfunction(f) and has_output_type(output_type, f)
    )

    # todo in the future sort the functions by Bayesian probabilities
    # funcs.sort(key=lambda f: (f.__code__.co_argcount, f.__code__.co_name))

    return funcs
