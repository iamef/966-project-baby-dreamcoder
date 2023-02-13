from dataclasses import dataclass
from typing import List, Tuple, Any


@dataclass(frozen=True)
class Problem:
    input_type: Tuple[type, ...]
    output_type: type
    input_ouput_pairs: List[Tuple[Tuple, Any]]


# EVERYTHING_ZERO_INPUT = Problem(
#     (Any,),
#     int,
#     [
#         (True, 0),
#         ([1, 2, 3], 0),
#         (134, 0),
#         (-1530, 0),
#         ((False, True), 0)
#     ]
# )