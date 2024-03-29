import functools

# YOU CAN CHOOSE WHICH PRIMITIVES TO USE HERE
# import primitives_induction as prim
# import primitives_number_game as prim
import primitives_ng_more_ints as prim

from problem import Problem
from interpreter import *

import inspect
import itertools
from typing import Tuple, List, Any, Callable


# NOTE FOR READER: THE MOST IMPORTANT FUNCTION IS
# generate_programs
# the rest are helper functions.


def has_output_type(output_type: type, f: callable):
    # a dictionary mapping variable names to types
    f_args_annotations = inspect.getfullargspec(f).annotations
    return 'return' in f_args_annotations and f_args_annotations['return'] is output_type


def get_functions_filtered(filt: Callable[[Tuple[Callable, str]], bool]) -> List[callable]:
    """

    :param filt: callable. input is a Tuple (function_name: string, function: callable)
                            output is a boolean indicating whether the function passes the filter or not
    :return: a list of functions in List[Tuple]
    """
    funcs = inspect.getmembers(prim, lambda f: inspect.isfunction(f) and filt(f))

    # sort functions by number of arguments, then by name
    funcs.sort(key=lambda f: (f[1].__code__.co_argcount, f[0]))

    return list(map(lambda f: f[1], funcs))


def get_functions_by_output_type(output_type: type) -> List[callable]:
    return get_functions_filtered(
        # the isfunction is not necessary, but redundancy is nice to avoid errors I guess
        lambda f: inspect.isfunction(f) and has_output_type(output_type, f)
    )


def func_composition_to_program(func_comp: List[List[Any]]) -> Program:
    """
    # each partial function ideally has format (some the lists may instead be in tuple format)
    # [
    #   [base func],
    #   [[args1, 2, ... of base func]],
    #   [[[args of args1 of base function], [args of args2]]]
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


def valid_programs_returns_input(problem: Problem, inp_type_var_map, func_args_type_map):
    """
    given a problem with multiple inputs
    this will generate programs that solve the problem by just returning one of the inputs as an output

    :param problem:
    :param inp_type_var_map:
    :return: valid programs that literally just returns one of the inputs
    """
    valid_funcs = []

    # first test if just returning the inputs work
    output_matching_inputs = inp_type_var_map.setdefault(problem.output_type, [])
    simple_func_input = tuple(output_matching_inputs)
    # simple_func_input = (simple_func_input,)  # technically we only have one input, so we put it all to a tuple
    for var in output_matching_inputs:
        inp = int(var.split("_")[1])

        # def prog(args): return args[inp]
        def program_factory(dont_change):
            return Program(lambda *args: args[dont_change], (*simple_func_input, inp))

        prog = program_factory(inp)

        # you can't do the below because the looping inp will update the
        # inp in valid_funcs which is quite bad... args[inp]
        # THIS DOESN'T WORK! prog = Program(lambda *args: args[inp], (*simple_func_input, inp))

        if test_program(problem, prog):  # if len(valid_funcs) == 0:
            # format [(var, prob of var)]
            var_prob = list(filter(lambda x: x[0] == var, func_args_type_map[problem.output_type]))

            # grab the prob of var in the format
            var_prob = var_prob[0][1]

            valid_funcs.append((prog, var_prob))

        # print(prog, valid_funcs[0])
        # print(prog.args, valid_funcs[0].args)
        # as you can see in this print statement,
        # the prog and valid_funcs will start matching because the inp update affects both of them
        # for the case prog = Program(lambda *args: args[inp]
        # print(interpret(prog, (42356, 1435, 123, 5, 176)), interpret(valid_funcs[0], (42356, 1435, 123, 5, 176)))

    return valid_funcs

def filling_probability_cartesian_product(func_args_to_cartesian: list[list[tuple]], min_prob: float) -> List[Tuple[Tuple, float]]:
    """
    :param func_args_to_cartesian:
    # format [[arg1 options], [arg2 options], [arg3 options]]
    # alternatively [[func1 options], [func2 options], [func3 options]]
    # each argi option is in the format (function, probability

    :return:
    [
        ((arg1_1, arg2_1, arg3_1), prob),
        ((arg1_2, ...
    }
    """
    cartesianed = list(itertools.product(*func_args_to_cartesian))

    def format_fll_option(bad_format_fill_option):
        # format of bad_format_fill_option (aka each element of cartesianed)
        # (
        #   (arg1_1, prob1), (arg2_1, prob2), (arg3_1, prob3)
        # )
        args = tuple(arg for arg, prob in bad_format_fill_option)

        # multiply all the probabilities in the list
        prob = functools.reduce(lambda prev, curr:  prev * curr[1], bad_format_fill_option, 1)

        return args, prob

    fillings_and_prob = list(map(format_fll_option, cartesianed))
    fillings_and_prob = list(filter(lambda arg_prob: arg_prob[1] > min_prob, fillings_and_prob))

    return fillings_and_prob


def get_all_function_specific_fillings(func: callable, inp_type_var_map: dict, func_args_type_map: dict,
                                       terminals_only: bool, min_prob: float) -> List[Tuple[Tuple[Any], float]]:
    func_args_annotations = inspect.getfullargspec(func).annotations
    del (func_args_annotations['return'])

    # format [[arg1 options], [arg2 options], [arg3 options]]
    func_args_to_cartesian = []
    for arg_type in func_args_annotations.values():

        this_func_args_and_prob = func_args_type_map[arg_type]  # todo if time figure out what to do if no functions exist

        # not relevant to numbers game, can incorporate later
        # if arg_type is callable and func.__name__ == "ind_int":
        #     this_func_args.extend(get_functions_by_output_type(int))

        # if we are at the last layer, and we just want terminals,
        # we don't want to be making and adding all these functions
        if terminals_only:
            this_func_args_and_prob = list(filter(lambda ap: ap[0] in inp_type_var_map[arg_type], this_func_args_and_prob))
            # this_func_args_and_prob = [(var, 1/len(inp_type_var_map[arg_type])) for var in inp_type_var_map[arg_type]]

        # filter min_prob early so that the cartesian product is easier
        this_func_args_and_prob = list(filter(lambda arg_prob: arg_prob[1] > min_prob, this_func_args_and_prob))

        func_args_to_cartesian.append(this_func_args_and_prob)

    ret = filling_probability_cartesian_product(func_args_to_cartesian, min_prob)

    return ret


def get_all_overall_fillings(func_composition: List[Any], inp_type_var_map: dict, func_args_type_map: dict,
                             terminals_only: bool, min_prob: float) -> List[Tuple[List[Any], float]]:
    """
    :param func_composition:
    :param inp_type_var_map:
    :param func_args_type_map:
    :param terminals_only:
    each partial function ideally has format (some the lists may instead be in tuple format)
    # [
    #   [base func],
    #   [[args1, 2, ... of base func]],
    #   [[[args of args1 of base function], [args of args2]]]
    # ]
    :return: all possitble function fillings along with their probabilities
    """

    def get_all_overall_fillings_helper(deep_func_list, parent=None):
        """

        :param deep_func_list: last line of the func_composition
        :return: tbd
        """
        # WORK IN PROGRESS ATTEMPT TO NOT FILL IN FUNCTION THAT IS AN ARGUMENT TO ANOTHER FUNCTION
        # if parent is None:
        #     # check for parent not being None
        #     if len(func_composition) > 2:
        #         parent = func_composition[-2]
        #     else:
        #         parent = [[]]
        #
        to_cartesian_prod = []

        for i, func_layer in enumerate(deep_func_list):
            # WORK IN PROGRESS ATTEMPT TO NOT FILL IN FUNCTION THAT IS AN ARGUMENT TO ANOTHER FUNCTION
            # i_parent = parent[i]

            if type(func_layer) is list or type(func_layer) is tuple:
                to_cartesian_prod.append(get_all_overall_fillings_helper(func_layer))
            elif not callable(func_layer):
                to_cartesian_prod.append([(tuple(), 1)])  # we don't want this to contribute to the cartesian product being empty
            # WORK IN PROGRESS ATTEMPT TO NOT FILL IN FUNCTION THAT IS AN ARGUMENT TO ANOTHER FUNCTION
            # elif callable(parent) and :
            #
            elif len(inspect.getfullargspec(func_layer).args) == 0:
                to_cartesian_prod.append([(tuple(), 1)])
            else:  # callable and has more than one argument
                to_cartesian_prod.append(
                    get_all_function_specific_fillings(func_layer, inp_type_var_map,
                                                       func_args_type_map, terminals_only, min_prob))

        # if any one of the lists are empty, then the cartesian product will be empty as well
        ret = filling_probability_cartesian_product(to_cartesian_prod, min_prob)
        return ret

    return get_all_overall_fillings_helper(func_composition[-1])


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


def get_inp_type_var_map(prob: Problem):
    inp_type_var_map = {}

    prob_num_inputs = len(prob.input_type)
    for i in range(prob_num_inputs):
        input_type = prob.input_type[i]

        if input_type not in inp_type_var_map:
            inp_type_var_map[input_type] = []
        inp_type_var_map[input_type].append("x_" + str(i))

    return inp_type_var_map


def get_func_probability_weight(f: callable, weights_by_type) -> float:
    f_argsspec = inspect.getfullargspec(f)

    f_args = f_argsspec.args

    # a dictionary mapping variable names to types
    f_args_annotations = f_argsspec.annotations

    input_type: tuple = tuple(f_args_annotations[arg] for arg in f_args)
    output_type: type = f_args_annotations['return']

    return weights_by_type.setdefault(output_type, dict()).setdefault(input_type, 0)


def get_func_args_type_probabilities_map(inp_type_var_map: dict,
                                         weights_by_type: dict[type, dict[Tuple[type, ...]], float]
                                         ) -> dict[type, List[Tuple[callable, float]]]:
    """
    :param inp_type_var_map:
    :param weights_by_type:
    :return:

    format  Dict[output_type, List[Tuple[func or var, probabilities]]
    """

    func_args_type_probabilities_map = {}

    for out_type, input_weight_dict in weights_by_type.items():
        func_args_type_probabilities_map[out_type] = []

        var_weights_list = inp_type_var_map.setdefault(out_type, [])
        var_weights_list = [(var, 1) for var in var_weights_list]

        func_weights_list = get_functions_by_output_type(out_type)
        func_weights_list = [(func, get_func_probability_weight(func, weights_by_type)) for func in func_weights_list]

        # sort functions by
        # (1) Bayesian probabilities (negative because want in descending order)
        # (2) number of args
        # (3) function name
        func_weights_list.sort(key=lambda f: (-f[1], f[0].__code__.co_argcount, f[0].__name__))

        norm_constant = sum([w for var, w in var_weights_list]) + sum([w for f, w in func_weights_list])

        func_args_type_probabilities_map[out_type].extend([(var, w / norm_constant) for var, w in var_weights_list])
        func_args_type_probabilities_map[out_type].extend([(func, w / norm_constant) for func, w in func_weights_list])

    return func_args_type_probabilities_map


def generate_programs(problem: Problem, max_depth=2, min_prob=1e-6) -> List[Tuple[Program, float]]:
    """
    THE MOST IMPORTANT FUNCTION IN THIS FILE!!!

    :param problem: input Problem for program to solve
    :param max_depth: max program depth (max number of times a function can call another function that
                                         calls another function)
    :param min_prob: program prior probability cutoff; all programs must have prior probability >= min_prob
    :return: A list of all the programs that solve the input problem.
             The return list comes in the form of (program, prior probability).
             The prior probability is the prior probabilities of each function used multiplied.
    """
    valid_funcs = []

    prob_num_inputs = len(problem.input_type)

    inp_type_var_map = get_inp_type_var_map(problem)

    # todo update the partial function format because it will now include probabilities
    # each partial function ideally has format (some lists may instead be in tuple format)
    # [
    #   [base func],
    #   [[args1, 2, ... of base func]],
    #   [[[args of args1 of base function], [args of args2]]]
    # ]
    func_args_type_probabilities_map = get_func_args_type_probabilities_map(inp_type_var_map, prim.prim_weights)

    # does a simple return one of the inputs
    # todo update this function to actually have return of function
    # todo alternatively, this won't be used at all in the number game
    valid_funcs.extend(valid_programs_returns_input(problem, inp_type_var_map, func_args_type_probabilities_map))

    funcs_to_complete_queue = [
        ([[f_and_prob[0]]], f_and_prob[1])  # ([[function]], probbability
        for f_and_prob in func_args_type_probabilities_map[problem.output_type] if callable(f_and_prob[0])
    ]

    while len(funcs_to_complete_queue) > 0:  # also figure out the depth situation
        func_composition, func_prob = funcs_to_complete_queue.pop(0)

        # stop the while loop when we hit max_depth
        # currently functions are in order of depth so should terminate when we reach first func that is > max_depth
        if len(func_composition) > max_depth:
            break

        # complete args for everything in the layer
        # todo make the terminals only thing dependendent on stuff, also there may be no fill in options
        fill_in_options = get_all_overall_fillings(func_composition, inp_type_var_map,
                                                   func_args_type_probabilities_map,
                                                   len(func_composition) == max_depth,
                                                   min_prob / func_prob)

        # test to see if fill in option is done (doesn't need substitutions anymore)
        for fill_in, fill_in_prob in fill_in_options:
            func_to_complete_plus_fill_in = [*func_composition, fill_in]
            fun_plus_fill_in_prob = func_prob * fill_in_prob

            if fun_plus_fill_in_prob < min_prob:
                continue

            done = fill_in_completes_function(fill_in, inp_type_var_map)

            if done:
                func_prog = func_composition_to_program(func_to_complete_plus_fill_in)
                if test_program(problem, func_prog):  # if len(valid_funcs) == 0:
                    valid_funcs.append((func_prog, fun_plus_fill_in_prob))
            else:
                funcs_to_complete_queue.append((func_to_complete_plus_fill_in, fun_plus_fill_in_prob))

    # sort functions by 1) probability 2) name
    valid_funcs.sort(key=lambda f_and_prob: (-f_and_prob[1], str(f_and_prob[0])))

    # todo probably normalize the probabilities for the functions
    return valid_funcs


def test_program(problem: Problem, prog: Program):
    """

    :param problem: input problem
    :param prog: program
    :return: True if the program solves the input problem, False if it doesn't
    """
    for inp, out in problem.input_ouput_pairs:
        try:
            if interpret(prog, inp) != out:
                return False
        except:  # because ind raises a ValueError when things are negative
            return False

    return True
