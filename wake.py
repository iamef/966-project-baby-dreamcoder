import primitives as prim
from problem import Problem
from interpreter import *

import inspect
import itertools
from typing import Tuple, List, Any, Callable


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
        if f_args_annotations[arg] in input_type:
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
    return f_args_annotations['return'] is output_type
    # f_return_annotation = inspect.signature(prim.zero).return_annotation
    #
    # type_overlap = set(f_return_annotation).intersection(set(output_type).union({Any}))
    #
    # return len(type_overlap) > 0


def get_functions_filtered(filt: Callable[[Tuple[Callable, str]], bool]) -> List[callable]:
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

    return list(map(lambda f: f[1], funcs))


def get_functions_by_types(input_type: Tuple[type, ...], output_type: type) -> List[callable]:
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


def get_functions_by_output_type(output_type: type) -> List[callable]:
    return get_functions_filtered(
        # todo the is function is not necessary
        lambda f: inspect.isfunction(f) and has_output_type(output_type, f)
    )


def func_composition_to_program(func_comp: List[List[Any]]) -> Program:
    """
    # each partial function has format
    # [
    #   [base func],
    #   [[args1, 2, ... of base func]],
    #   [[args of args1 of base function], [args of args2]] <-- todo maybe this has more brackets idk
    # ]
    :return: Program
    """
    prog_func = func_comp[0][0]
    prog_args = []

    for arg_i, arg in enumerate(func_comp[1][0]):
        if not callable(arg):
            prog_args.append(arg)
        else:
            sub_func_comp = [layer[arg_i] for layer in func_comp[1:]]
            prog_args.append(func_composition_to_program(sub_func_comp))

    return Program(prog_func, tuple(prog_args))



def valid_programs_returns_input(prob: Problem, inp_type_var_map):
    """
    given a problem with multiple inputs
    this will generate programs that solve the problem by just returning one of the inputs as an output

    :param prob:
    :param inp_type_var_map:
    :return:
    """
    valid_funcs = []

    # first test if just returning the inputs work
    output_matching_inputs = inp_type_var_map.setdefault(prob.output_type, [])
    simple_func_input = tuple(output_matching_inputs)
    # simple_func_input = (simple_func_input,)  # technically we only have one input so we put it all to a tuple
    for inp in map(lambda s: int(s.split("_")[1]), output_matching_inputs):
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
        # the prog and valid_funcs will start matching because the inp update affects both of them
        # for the case prog = Program(lambda *args: args[inp]
        # print(interpret(prog, (42356, 1435, 123, 5, 176)), interpret(valid_funcs[0], (42356, 1435, 123, 5, 176)))

    return valid_funcs



def generate_programs(prob: Problem, max_depth=2) -> List[Program]:
    valid_funcs = []

    prob_num_inputs = len(prob.input_type)

    inp_type_var_map = {}
    for i in range(prob_num_inputs):
        input_type = prob.input_type[i]

        if input_type not in inp_type_var_map:
            inp_type_var_map[input_type] = []
        inp_type_var_map[input_type].append("x_" + str(i))

    valid_funcs.extend(valid_programs_returns_input(prob, inp_type_var_map))

    # each partial function has format
    # [
    #   [base func],
    #   [args1, 2, ... of base func],
    #   [[args of args1 of base function], [args of args2]]
    # ]
    func_args_type_map = {}
    funcs_to_complete_queue = [[[func]] for func in get_functions_by_output_type(prob.output_type)]

    while len(funcs_to_complete_queue) > 0:  # also figure out the depth situation
        func_composition = funcs_to_complete_queue.pop(0)

        # stop the while loop when we hit max_depth
        # currently functions are in order of depth
        # so this should terminate when we reach the first func that is > max_depth
        if len(func_composition) > max_depth:
            break

        # complete args for everything in the layer
        fill_in_options = []

        for func in func_composition[-1]:
            if not callable(func):
                fill_in_options.append([])
                continue
            func_args_annotations = inspect.getfullargspec(func).annotations
            del(func_args_annotations['return'])

            if len(func_args_annotations) == 0:
                fill_in_options.append([[]])
                continue

            # args for just the particular function
            func_args_fill_in = []
            for arg_type in func_args_annotations.values():

                if arg_type not in func_args_type_map:
                    func_args_type_map[arg_type] = []
                    func_args_type_map[arg_type].extend(inp_type_var_map.setdefault(arg_type, []))
                    func_args_type_map[arg_type].extend(get_functions_by_output_type(arg_type))
                this_func_args = func_args_type_map[arg_type]

                if len(func_args_fill_in) == 0:
                    func_args_fill_in.extend([[arg] for arg in this_func_args])
                else:
                    # TODO
                    old_func_args = func_args_fill_in.copy()
                    func_args_fill_in = []
                    for arg in this_func_args:
                        func_args_fill_in.extend([[*old_func_arg, arg] for old_func_arg in old_func_args])


            if len(fill_in_options) == 0:
                fill_in_options.extend([[arg] for arg in func_args_fill_in])
            else:
                old_fill_in_options = fill_in_options.copy()
                fill_in_options = []
                for arg in func_args_fill_in:
                    fill_in_options.extend([[*old_fill_in, arg] for old_fill_in in old_fill_in_options])


        # test to see if fill in option is done (doesn't need substitutions anymore)
        for fill_in in fill_in_options:
            done = True

            func_to_complete_plus_fill_in = [*func_composition, fill_in]

            for func_args in fill_in:
                for func_arg in func_args:
                    if func_arg not in [arg for sublist in inp_type_var_map.values() for arg in sublist]:
                        done = False
                        break

            if done:
                func_prog = func_composition_to_program(func_to_complete_plus_fill_in)
                if test_program(prob, func_prog):  # if len(valid_funcs) == 0:
                    valid_funcs.append(func_prog)
            else:
                funcs_to_complete_queue.append(func_to_complete_plus_fill_in)

    return valid_funcs


def test_program(problem: Problem, prog: Program):  # figure out how to make a program out of this...
    for inp, out in problem.input_ouput_pairs:
        if interpret(prog, inp) != out:
            return False

    return True
