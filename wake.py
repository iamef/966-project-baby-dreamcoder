import primitives_induction as prim
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
    # each partial function ideally has format (some of the the lists may instead be in tuple format)
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
            # extra [0] because there is extra [] in arg of base func that trickles down
            sub_func_comp = [[layer[0][arg_i]] for layer in func_comp[1:]]
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


def cartesian_product(list1, list2):
    pass


def get_all_function_specific_fillings(func: callable, inp_type_var_map: dict, func_args_type_map: dict):
    func_args_annotations = inspect.getfullargspec(func).annotations
    del (func_args_annotations['return'])

    # format [[arg1 options], [arg2 options], [arg3 options]]
    func_args_to_cartesian = []
    for arg_type in func_args_annotations.values():

        if arg_type not in func_args_type_map:
            func_args_type_map[arg_type] = []
            func_args_type_map[arg_type].extend(inp_type_var_map.setdefault(arg_type, []))
            func_args_type_map[arg_type].extend(get_functions_by_output_type(arg_type))

        this_func_args = func_args_type_map[arg_type]
        if arg_type is callable and func.__name__ == "ind_int":
            this_func_args.extend(get_functions_by_output_type(int))

        func_args_to_cartesian.append(this_func_args)

        # personal attempt at doing cartesian product...
        # if len(func_args_to_cartesian) == 0:
        #     func_args_fill_in.extend([[arg] for arg in this_func_args])
        # else:
        #     # TODO
        #     old_func_args = func_args_fill_in.copy()
        #     func_args_fill_in = []
        #     for arg in this_func_args:
        #         func_args_fill_in.extend([[*old_func_arg, arg] for old_func_arg in old_func_args])

    ret = list(itertools.product(*func_args_to_cartesian))
    return ret


def get_all_overall_fillings(func_composition: List[Any], inp_type_var_map: dict, func_args_type_map: dict,
                             terminals_only):
    """

    :param func_args_type_map:
    :param inp_type_var_map:
    :param func_composition:
    each partial function ideally has format (some of the the lists may instead be in tuple format)
    # [
    #   [base func],
    #   [[args1, 2, ... of base func]],
    #   [[args of args1 of base function], [args of args2]] <-- todo maybe this has more brackets idk
    # ]
    :return: all possitble function fillings
    """

    def get_all_overall_fillings_helper(deep_func_list):
        """

        :param deep_func_list: last line of the func_composition
        :return: tbd
        """
        to_cartesian_prod = []
        # if type(deep_func_list) is not list:
        #     deep_func_list = list(deep_func_list)

        for func_layer in deep_func_list:
            if type(func_layer) is list or type(func_layer) is tuple:
                to_cartesian_prod.append(get_all_overall_fillings_helper(func_layer))
            elif not callable(func_layer):
                to_cartesian_prod.append([])
            elif len(inspect.getfullargspec(func_layer).args) == 0:
                to_cartesian_prod.append([[]])
            else:  # callable and has more than one argument
                to_cartesian_prod.append(
                    get_all_function_specific_fillings(func_layer, inp_type_var_map, func_args_type_map))

        ret = list(itertools.product(*to_cartesian_prod))
        return ret

    return get_all_overall_fillings_helper(func_composition[-1])

    # fill_in_options

    # for func in func_composition[-1]:
        # if not callable(func):
        #     fill_in_options.append([])
        #     continue
        # func_args_annotations = inspect.getfullargspec(func).annotations
        # del (func_args_annotations['return'])
        #
        # if len(func_args_annotations) == 0:
        #     fill_in_options.append([[]])
        #     continue

        # args for just the particular function
        # func_args_fill_in = []
        # for arg_type in func_args_annotations.values():
        #
        #     if arg_type not in func_args_type_map:
        #         func_args_type_map[arg_type] = []
        #         func_args_type_map[arg_type].extend(inp_type_var_map.setdefault(arg_type, []))
        #         func_args_type_map[arg_type].extend(get_functions_by_output_type(arg_type))
        #     this_func_args = func_args_type_map[arg_type]
        #
        #     if len(func_args_fill_in) == 0:
        #         func_args_fill_in.extend([[arg] for arg in this_func_args])
        #     else:
        #         # TODO
        #         old_func_args = func_args_fill_in.copy()
        #         func_args_fill_in = []
        #         for arg in this_func_args:
        #             func_args_fill_in.extend([[*old_func_arg, arg] for old_func_arg in old_func_args])

        # if len(fill_in_options) == 0:
        #     fill_in_options.extend([[arg] for arg in func_args_fill_in])
        # else:
        #     old_fill_in_options = fill_in_options.copy()
        #     fill_in_options = []
        #     for arg in func_args_fill_in:
        #         fill_in_options.extend([[*old_fill_in, arg] for old_fill_in in old_fill_in_options])


def fill_in_completes_function(fill_in, inp_type_var_map: dict) -> bool:
    for func_layer in fill_in:
        if type(func_layer) is list or type(func_layer) is tuple:
            if not fill_in_completes_function(func_layer, inp_type_var_map):
                return False
        else:
            terminals_list = [arg for sublist in inp_type_var_map.values() for arg in sublist]
            if func_layer not in terminals_list:
                return False

    return True


def generate_programs(prob: Problem, max_depth=2) -> List[Program]:
    valid_funcs = []

    prob_num_inputs = len(prob.input_type)

    inp_type_var_map = {}
    for i in range(prob_num_inputs):
        input_type = prob.input_type[i]

        if input_type not in inp_type_var_map:
            inp_type_var_map[input_type] = []
        inp_type_var_map[input_type].append("x_" + str(i))

    # does a simple return one of the inputs
    valid_funcs.extend(valid_programs_returns_input(prob, inp_type_var_map))

    # each partial function ideally has format (some of the the lists may instead be in tuple format)
    # [
    #   [base func],
    #   [[args1, 2, ... of base func]],
    #   [[args of args1 of base function], [args of args2]] <-- todo maybe this has more brackets idk
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
        # todo make the terminals only thing dependendent on stuff, also there may be no fill in options
        fill_in_options = get_all_overall_fillings(func_composition, inp_type_var_map, func_args_type_map, False)

        # test to see if fill in option is done (doesn't need substitutions anymore)
        for fill_in in fill_in_options:
            # done = True

            func_to_complete_plus_fill_in = [*func_composition, fill_in]

            # for func_args in fill_in:
            #     for func_arg in func_args:
            #         if func_arg not in [arg for sublist in inp_type_var_map.values() for arg in sublist]:
            #             done = False
            #             break

            done = fill_in_completes_function(fill_in, inp_type_var_map)

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
