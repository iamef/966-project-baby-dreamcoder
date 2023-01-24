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


def generate_programs(prob: Problem, depth=5) -> List[Program]:
    valid_funcs = []

    funcs_to_complete_queue = [None]

    prob_num_inputs = len(prob.input_type)

    inp_type_var_map = {}
    for i in range(prob_num_inputs):
        input_type = prob.input_type[i]

        if input_type not in inp_type_var_map:
            inp_type_var_map[input_type] = [i]
        else:
            inp_type_var_map[input_type].append(i)

    # first test if just returning the inputs work
    output_matching_inputs = inp_type_var_map.setdefault(prob.output_type, [])
    simple_func_input = tuple("x_" + str(i) for i in range(len(output_matching_inputs)))
    # simple_func_input = (simple_func_input,)  # technically we only have one input so we put it all to a tuple
    for inp in inp_type_var_map.setdefault(prob.output_type, []):
        # def prog(args): return args[inp]
        def program_factory(dont_change):
            return Program(lambda *args: args[dont_change], (*simple_func_input, inp))

        prog = program_factory(inp)

        # you can't do the below because the looping inp will update the
        # inp in valid_funcs which is quite bad... args[inp]
        # THIS DOESN'T WORK! prog = Program(lambda *args: args[inp], (*simple_func_input, inp))

        if test_program(prob, prog):  # if len(valid_funcs) == 0:
            valid_funcs.append(prog)

        # print(prog, valid_funcs[0])
        # print(prog.args, valid_funcs[0].args)
        # as you can see in this print statement,
        # the prog and valid_funcs start will  matching because the inp update affects both of them
        # for the case prog = Program(lambda *args: args[inp]
        # print(interpret(prog, (42356, 1435, 123, 5, 176)), interpret(valid_funcs[0], (42356, 1435, 123, 5, 176)))

    return valid_funcs

    # # terminals = [prim.zero].extend(range(prob_num_inputs))
    # # terminals = list(range(prob_num_inputs))
    # # # funcs_to_complete_queue.extend(terminals)
    #
    # layer1 = get_functions_by_types(prob.input_type, prob.output_type)
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


def test_program(problem: Problem, prog: Program):  # figure out how to make a program out of this...
    for inp, out in problem.input_ouput_pairs:
        if interpret(prog, inp) != out:
            return False

    return True
