import primitives as prim

import inspect
from typing import Tuple, List, Any


def get_functions_by_types(input_type: Tuple[type, ...], output_type: Tuple[type, ...]) -> List[callable]:
    """
    gets function with at least one of the input types

    returns function in order of least number of inputs to most number of inputs
    """

    def has_input_type(f: callable):
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

        # type_overlap = set(f_args_annotations.values()).intersection(set(input_type).union({Any}))
        # # reminder to add the any type
        #
        # return len(type_overlap) > 0

    def has_output_type(f: callable):
        # todo figure this part out
        return True

        # a dictionary mapping variable names to types
        f_args_annotations = inspect.getfullargspec(f).annotations
        return f_args_annotations['return'] is Any or f_args_annotations['return'] is output_type
        # f_return_annotation = inspect.signature(prim.zero).return_annotation
        #
        # type_overlap = set(f_return_annotation).intersection(set(output_type).union({Any}))
        #
        # return len(type_overlap) > 0

    def is_right_type(f):
        return inspect.isfunction(f) and has_input_type(f) and has_output_type(f)







    funcs = inspect.getmembers(prim, is_right_type)

    # sort functions by number of arguments, then by name
    # todo in the future sort the functions by Bayesian probabilities
    funcs.sort(key=lambda f: (f.__code__.co_argcount, f.__code__.co_name))

    return funcs
