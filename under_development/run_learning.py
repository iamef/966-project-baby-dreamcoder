from wake import *



positive_plus_problem = Problem(
    input_type=(int, int),
    output_type=int,
    input_ouput_pairs=[
        ((1, 5), 7),  # 123, 5, 176
        ((3, 2), 5),  # 1342, 814, 132
        ((4, 7), 11),  # 8, 3, 1
        ((2, 6), 8),  # 27, 83, 34
        ((5, 6), 11)  # 92, 74, 63
    ]
)

out_progs = generate_programs(positive_plus_problem)

for out_prog, prog_prob in out_progs:
    for inp, out in positive_plus_problem.input_ouput_pairs:
        actual_res: int = interpret(out_prog, inp)
        # self.assertEqual(actual_res, out)
        print(actual_res == out, actual_res, out)
    print(prog_prob, out_prog)


