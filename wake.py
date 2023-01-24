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


# TO_FILL = None
# class FunctionBuilder:
#     def __init__(self, initial_func=None, output_type=type(None)):
#         if initial_func is None:
#             self.func_tree = []
#             self.missing_components = None
#         elif callable(initial_func):
#             self.func_tree = [initial_func]
#             self.missing_components =
#         # elif type(initial_func) is list:
#         #     self.func_tree = initial_func
#         else:
#             raise TypeError("initial_func must be None, Callable, or function tree")
#
#         self.check_func_tree()
#
#     def check_func_tree(self, func_tree: None):
#         if func_tree is None:
#             func_tree = self.func_tree
#
#         if len(func_tree) == 0:
#             return











def generate_function(problem: Problem, depth=5):
    function_layers = []

    funcs_to_complete_queue = [None]

    prob_num_inputs = len(problem.input_type)

    input_type_order_map = {}
    for i in range(prob_num_inputs):
        input_type = problem.input_type[i]

        if input_type not in input_type_order_map:
            input_type_order_map[input_type] = [i]
        else:
            input_type_order_map[input_type].append(i)

    # first test if just returning the inputs work
    for inp in input_type_order_map.setdefault(problem.output_type, []):
        func = lambda args: args[inp]
        if test_function(problem, func):
            return func



    # # terminals = [prim.zero].extend(range(prob_num_inputs))
    # # terminals = list(range(prob_num_inputs))
    # # # funcs_to_complete_queue.extend(terminals)
    #
    # layer1 = get_functions_by_types(problem.input_type, problem.output_type)
    # funcs_to_complete_queue.extend(layer1)
    #
    # while len(funcs_to_complete_queue) > 0:
    #     func_composition = funcs_to_complete_queue.pop(0)
    #
    #     # find missing part
    #
    #     #     todo maybe it would actually be easier to make this stuff into a list...
    #
    #
    #
    #     # do some test to make program complete in some way
    #
    # # def complete_function(func_composition):
    # #`


def test_function(problem: Problem, func: callable):  # figure out how to make a program out of this...
    for inp, out in problem.input_ouput_pairs:
        if func(inp) != out:
            return False

    return True



