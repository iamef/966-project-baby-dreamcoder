from wake import *


double_problem = Problem(
    input_type=(int,),
    output_type=int,
    input_ouput_pairs=[
        ((1,), 2),
        ((3,), 6),
        ((4,), 8),
        ((2,), 4),
        ((5,), 10)
    ]
)

double_out_progs = generate_programs(double_problem)

# for out_prog, prog_prob in out_progs:
#     for inp, out in double_problem.input_ouput_pairs:
#         actual_res: int = interpret(out_prog, inp)
#         # self.assertEqual(actual_res, out)
#         print(actual_res == out, actual_res, out)
#     print(prog_prob, out_prog)

triple_problem = Problem(
    input_type=(int,),
    output_type=int,
    input_ouput_pairs=[
        ((1,), 3),
        ((3,), 9),
        ((4,), 12),
        ((2,), 6),
        ((5,), 15)
    ]
)
triple_out_progs = generate_programs(triple_problem)


square_problem = Problem(
    input_type=(int,),
    output_type=int,
    input_ouput_pairs=[
        ((1,), 1),
        ((3,), 9),
        ((4,), 16),
        ((2,), 4),
        ((5,), 25)
    ]
)
square_out_progs = generate_programs(square_problem)



# positive_plus_problem = Problem(
#     input_type=(int, int),
#     output_type=int,
#     input_ouput_pairs=[
#         ((1, 5), 7),  # 123, 5, 176
#         ((3, 2), 5),  # 1342, 814, 132
#         ((4, 7), 11),  # 8, 3, 1
#         ((2, 6), 8),  # 27, 83, 34
#         ((5, 6), 11)  # 92, 74, 63
#     ]
# )
#
# out_progs = generate_programs(positive_plus_problem)
#
# for out_prog, prog_prob in out_progs:
#     for inp, out in positive_plus_problem.input_ouput_pairs:
#         actual_res: int = interpret(out_prog, inp)
#         # self.assertEqual(actual_res, out)
#         print(actual_res == out, actual_res, out)
#     print(prog_prob, out_prog)


