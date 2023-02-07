import unittest

import bayes
import primitives_induction as primi
from handcoded_to_learn import *
from wake import *
from interpreter import *


class TestInductionPrimitives(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(primi.zero(), 0, "zero method should return 0")

    def test_pred(self):
        self.assertEqual(primi.pred(5), 4, "pred of 5 should be 4")
        self.assertEqual(primi.pred(1), 0, "pred of 1 should be 0")
        self.assertEqual(primi.pred(0), -1, "pred of 0 should be -1")
        self.assertEqual(primi.pred(-10), -11, "pred of -10 should be -11")

    def test_succ(self):
        self.assertEqual(primi.succ(4), 5, "succ of 4 should be 5")
        self.assertEqual(primi.succ(0), 1, "succ of 0 should be 1")
        self.assertEqual(primi.succ(-1), 0, "succ of -1 should be 0")
        self.assertEqual(primi.succ(-11), -10, "succ of -11 should be -10")

    def test_neg(self):
        self.assertEqual(primi.neg(primi.zero()), primi.zero())
        self.assertEqual(primi.neg(1), -1)
        self.assertEqual(primi.neg(-9), 9)

    # def test_equal(self):
    #     self.assertTrue(primi.eq(primi.zero(), 0), "eq(zero(), 0) should return true")
    #     self.assertTrue(primi.eq(5, 5), "eq(5, 5) should return true")
    #     self.assertTrue(primi.eq(-11, -11), "eq(-11, -11) should return true")
    #     self.assertFalse(primi.eq(-10, 10), "eq(-10, 10) should return false")
    #     self.assertFalse(primi.eq(5, 8), "eq(9, 8) should return false")

    def test_less_than(self):
        self.assertFalse(primi.less_than(primi.zero(), 0), "less_than(zero(), 0) should return false")
        self.assertTrue(primi.less_than(-10, 10), "less_than(-10, 10) should return True")
        self.assertTrue(primi.less_than(5, 8), "less_than(5, 8) should return True")
        self.assertFalse(primi.less_than(11, 10), "less_than(11, 10) should return false")

    # def test_conj(self):
    #     self.assertTrue(primi.conj(True, True), "T and T should be T")
    #     self.assertFalse(primi.conj(True, False))
    #     self.assertFalse(primi.conj(False, True))
    #     self.assertFalse(primi.conj(False, False))
    #
    # def test_disj(self):
    #     self.assertTrue(primi.disj(True, True), "T and T should be T")
    #     self.assertTrue(primi.disj(True, False))
    #     self.assertTrue(primi.disj(False, True))
    #     self.assertFalse(primi.disj(False, False))

    def test_cond(self):
        self.assertEqual(primi.cond(True, primi.zero(), primi.succ(primi.zero())), primi.zero())
        self.assertEqual(primi.cond(False, True, False), False)

    def test_ind(self):
        with self.assertRaises(ValueError):
            primi.ind(primi.zero(), primi.pred(primi.zero()), primi.succ)
        self.assertEqual(primi.ind(primi.zero(), primi.zero(), primi.succ), 0)
        self.assertEqual(primi.ind(primi.zero(), primi.succ(primi.succ(primi.succ(primi.zero()))), primi.succ), 3)
        self.assertEqual(primi.ind(primi.zero(), primi.succ(primi.succ(primi.succ(primi.succ(primi.succ(primi.zero()))))), primi.pred), -5)


class TestHandcodedThingsToLearn(unittest.TestCase):
    def test_positive_plus(self):
        self.assertEqual(positive_plus(1, 3), 4)
        self.assertEqual(positive_plus(0, 10), 10)
        self.assertEqual(positive_plus(46, 589), 635)

    def test_plus(self):
        self.assertEqual(plus(0, 0), 0)
        self.assertEqual(plus(2, 0), 2)
        self.assertEqual(plus(0, 10), 10)
        self.assertEqual(plus(46, 589), 635)
        self.assertEqual(plus(-549, 59), -490)
        self.assertEqual(plus(320, -29), 291)


class TestInterpreter(unittest.TestCase):
    def test_interpreter_by_layers(self):
        # ONE LAYER CASES
        # zero arg case
        zero_arg_prog = Program(primi.zero, tuple())
        self.assertEqual(interpret(zero_arg_prog), 0)
        # one arg case
        one_arg_prog = Program(primi.neg, (1,))
        self.assertEqual(interpret(one_arg_prog), -1)
        # two+ args case
        two_arg_prog = Program(primi.less_than, (4, 5))
        self.assertEqual(interpret(two_arg_prog), True)
        three_arg_prog = Program(primi.ind, (0, 5, primi.pred))
        self.assertEqual(interpret(three_arg_prog), -5)
        positive_plus_prog = Program(primi.ind, (5, 7, primi.succ))
        self.assertEqual(interpret(positive_plus_prog), 12)

        # TWO LAYER CASES
        # one 2 layer, no other args
        just_two_layer_prog = Program(primi.succ, (Program(primi.succ, (7,)),))
        self.assertEqual(interpret(just_two_layer_prog), 9)
        # one 2 layers, one 1 layer
        # two_layer_one_layer_prog = Program(eq, (
        #     -7,
        #     Program(primi.neg, (7,))
        # ))
        # self.assertEqual(interpret(two_layer_one_layer_prog), True)

        # THREE or MORE LAYER CASES
        # one 6 layer case
        six_layer_prog = Program(
            primi.pred, (
                Program(primi.pred, (
                    Program(primi.pred, (
                        Program(primi.neg, (
                            Program(
                                primi.succ, (Program(primi.zero, tuple()),)
                            ),
                        )),
                    )),
                )),
            )
        )
        self.assertEqual(interpret(six_layer_prog), -4)

    def test_interpreter_plus(self):
        # def get_plus_prog(num1, num2):
        #     ind(num1,
        #          cond(
        #              less_than(zero(), num2),
        #              num2,  # num2 positive case
        #              neg(num2)  # num2 negative case
        #          ),
        #          cond(
        #              less_than(zero(), num2),
        #              succ,  # num2 positive case
        #              pred  # num2 negative case
        #          )
        #      )

        # plus
        num1 = -8
        num2 = -9

        plus_prog = Program(primi.ind_int, (
            num1,
            Program(primi.cond_int, (
                Program(primi.less_than, (Program(primi.zero, tuple()), num2)),
                num2,  # num2 positive case
                Program(primi.neg, (num2,))  # num2 negative case TODO this is bad
            )),
            Program(primi.cond_int, (
                Program(primi.less_than, (Program(primi.zero, tuple()), num2)),
                primi.succ,  # num2 positive case
                primi.pred  # num2 negative case
            ))
        ))

        self.assertEqual(interpret(plus_prog), -17)


class TestWake(unittest.TestCase):
    # def test_get_filtered_funcs_probabilities(self):
    #     fps = get_filtered_funcs_probabilities(lambda x: True, bayes.ng_prim_weights)
    #
    #     self.assertAlmostEqual(sum([t[1] for t in fps]), 1)
    #
    #     # for primitives_induction results should be the below
    #     # [(<function zero at 0x12db1b550>, 0.15306122448979592),
    #     # (<function neg at 0x12db1b700>, 0.15306122448979592),
    #     # (<function pred at 0x12db1b5e0>, 0.15306122448979592),
    #     # (<function succ at 0x12db1b670>, 0.15306122448979592),
    #     # (<function less_than at 0x12db1b790>, 0.15306122448979592),
    #     # (<function cond_func at 0x12db1b940>, 0.15306122448979592),
    #     # (<function cond_int at 0x12db1b8b0>, 0.05102040816326531),
    #     # (<function ind_int at 0x12db1ba60>, 0.030612244897959186),
    #     # (<function cond at 0x12db1b820>, 0.0),
    #     # (<function ind at 0x12db1b9d0>, 0.0)]
    #
    #     # for primitives_number_game
    #     # [(< function zero at 0x12b13b280 >, 0.08823529411764706),
    #     #  (< function neg at 0x12b13b430 >, 0.08823529411764706),
    #     #  (< function pred at 0x12b13b310 >, 0.08823529411764706),
    #     #  (< function succ at 0x12b13b3a0 >, 0.08823529411764706),
    #     #  (< function divisible_by at 0x12b13b9d0 >, 0.08823529411764706),
    #     #  (< function eq at 0x12b13b4c0 >, 0.08823529411764706),
    #     #  (< function less_than at 0x12b13b550 >, 0.08823529411764706),
    #     #  (< function mul at 0x12b13b940 >, 0.08823529411764706),
    #     #  (< function plus at 0x12b13b8b0 >, 0.08823529411764706),
    #     #  (< function cond_func at 0x12b13b820 >, 0.08823529411764706),
    #     #  (< function conj at 0x12b13b5e0 >, 0.04411764705882353),
    #     #  (< function disj at 0x12b13b670 >, 0.04411764705882353),
    #     #  (< function cond_int at 0x12b13b790 >, 0.029411764705882356), (< function cond at 0x12b13b700 >, 0.0)]


    def test_get_func_args_type_probabilities_map(self):
        out_dict_func_probs = get_func_args_type_probabilities_map({}, prim.ng_prim_weights)
        self.assertAlmostEqual(sum([t[1] for t in out_dict_func_probs[int]]), 1)
        # # [(< function zero at 0x12b73f310 >, 0.15789473684210528),
        # #  (< function neg at 0x12b73f430 >, 0.15789473684210528),
        # #  (< function pred at 0x12b73f280 >, 0.15789473684210528),
        # #  (< function succ at 0x12b73f3a0 >, 0.15789473684210528),
        # #  (< function mul at 0x12b73f940 >, 0.15789473684210528),
        # #  (< function plus at 0x12b73f8b0 >, 0.15789473684210528),
        # #  (< function cond_int at 0x12b73f790 >, 0.05263157894736842)]
        #
        # bool_func_probs = get_function_probabilities_by_output_type(bool, bayes.ng_prim_weights)
        self.assertAlmostEqual(sum([t[1] for t in out_dict_func_probs[bool]]), 1)
        # # [(< function divisible_by at 0x12b765700 >, 0.25),
        # #  (< function eq at 0x12b7651f0 >, 0.25),
        # #  (< function less_than at 0x12b765280 >, 0.25),
        # #  (< function conj at 0x12b765310 >, 0.125),
        # #  (< function disj at 0x12b7653a0 >, 0.125)
        # # ]
        #
        # callable_func_probs = get_function_probabilities_by_output_type(callable, bayes.ng_prim_weights)
        self.assertAlmostEqual(sum([t[1] for t in out_dict_func_probs[callable]]), 1)


        out_dict_func_probs = get_func_args_type_probabilities_map(
            {int: ["x_0", "x_1", "x_3"], bool: ["x_2"]},
            prim.ng_prim_weights
        )
        self.assertAlmostEqual(sum([t[1] for t in out_dict_func_probs[int]]), 1)
        self.assertAlmostEqual(sum([t[1] for t in out_dict_func_probs[bool]]), 1)
        self.assertAlmostEqual(sum([t[1] for t in out_dict_func_probs[callable]]), 1)


    # def test_get_functions_by_types(self):
    #     self.assertEqual(1, 1)
    #     int_inputs_actual = get_functions_by_types((int,), int)
    #     bool_inputs_actual = get_functions_by_types((bool,), bool)

    def test_filling_probability_cartesian_product(self):
        # to_cartesian = [(("stuf1_1", "stuf1_2"), 0.5), (("stuf2",), 0.5)]
        # expected = [((("stuf1_1", "stuf1_2"), ("stuf2",)), 0.25)]
        # self.assertListEqual(filling_probability_cartesian_product(to_cartesian), expected)
        #
        # to_cartesian = [[("arg1_1", 1), ("arg1_2", 2), ("arg1_3", 3)], [("arg2_1", 21), ("arg2_2", 22), ("arg2_3", 23)],
        #                 [("arg3_1", 31), ("arg3_2", 32)]]

        # expected = [(('arg1_1', 'arg2_1', 'arg3_1'), 651), (('arg1_1', 'arg2_1', 'arg3_2'), 672),
        #  (('arg1_1', 'arg2_2', 'arg3_1'), 682), (('arg1_1', 'arg2_2', 'arg3_2'), 704),
        #  (('arg1_1', 'arg2_3', 'arg3_1'), 713), (('arg1_1', 'arg2_3', 'arg3_2'), 736),
        #  (('arg1_2', 'arg2_1', 'arg3_1'), 1302), (('arg1_2', 'arg2_1', 'arg3_2'), 1344),
        #  (('arg1_2', 'arg2_2', 'arg3_1'), 1364), (('arg1_2', 'arg2_2', 'arg3_2'), 1408),
        #  (('arg1_2', 'arg2_3', 'arg3_1'), 1426), (('arg1_2', 'arg2_3', 'arg3_2'), 1472),
        #  (('arg1_3', 'arg2_1', 'arg3_1'), 1953), (('arg1_3', 'arg2_1', 'arg3_2'), 2016),
        #  (('arg1_3', 'arg2_2', 'arg3_1'), 2046), (('arg1_3', 'arg2_2', 'arg3_2'), 2112),
        #  (('arg1_3', 'arg2_3', 'arg3_1'), 2139), (('arg1_3', 'arg2_3', 'arg3_2'), 2208)]
        #
        # self.assertListEqual(filling_probability_cartesian_product(to_cartesian), expected)

    def test_get_all_function_specific_fillings(self):
        funcs = get_functions_by_output_type(int)

        inp_type_var_map = {int: ["x_0", "x_1", "x_3"], bool: ["x_2"]}
        out_dict_func_probs = get_func_args_type_probabilities_map(inp_type_var_map, prim.ng_prim_weights)

        for func in funcs:
            print(func.__name__)
            aooke = get_all_function_specific_fillings(func, inp_type_var_map, out_dict_func_probs, False)
            print(aooke, False)
            self.assertAlmostEqual(sum([t[1] for t in aooke]), 1)

            aooke = get_all_function_specific_fillings(func, inp_type_var_map, out_dict_func_probs, True)
            print(aooke, True)
            self.assertAlmostEqual(sum([t[1] for t in aooke]), 1)


    def test_get_all_overall_fillings(self):
        func_comp = [
            primi.cond,
            [primi.less_than, primi.succ, primi.pred],
            [[primi.succ, primi.pred], [primi.zero], [primi.pred]]
        ]

        inp_type_var_map = {int: ["x_0", "x_1", "x_3"], bool: ["x_2"]}
        func_args_type_map = get_func_args_type_probabilities_map(inp_type_var_map, prim.ng_prim_weights)

        fillings_all = get_all_overall_fillings(func_comp, inp_type_var_map, func_args_type_map, False)
        fillings_terminals_only = get_all_overall_fillings(func_comp, inp_type_var_map, func_args_type_map, True)

        print(fillings_all)
        print(fillings_terminals_only)

    def test_generate_function(self):
        first_input_problem = Problem(
            input_type=(int, int),
            output_type=int,
            input_ouput_pairs=[
                ((42, 14), 42),  # 123, 5, 176
                ((1, 2), 1),  # 1342, 814, 132
                ((4, 2), 4),  # 8, 3, 1
                ((8, 26), 8),  # 27, 83, 34
                ((7, 56), 7)  # 92, 74, 63
            ]
        )

        out_progs = generate_programs(first_input_problem)

        for out_prog, prog_prob in out_progs:
            for inp, out in first_input_problem.input_ouput_pairs:
                actual_res: int = interpret(out_prog, inp)
                self.assertEqual(actual_res, out)
                # print(actual_res == out, actual_res, out)
            print(prog_prob, out_prog)

        # everything_zero_problem = Problem(
        #     input_type=(Any,),
        #     output_type=int,
        #     input_ouput_pairs=[
        #         (True, 0),
        #         ([1, 2, 3], 0),
        #         (134, 0),
        #         (-1530, 0),
        #         ((False, True), 0)
        #     ]
        # )
        # actually

        # out_progs = generate_programs(everything_zero_problem)
        #
        # for out_prog in out_progs:
        #     for inp, out in everything_zero_problem.input_ouput_pairs:
        #         actual_res: int = interpret(out_prog, inp)
        #         print(actual_res == out, actual_res, out)


if __name__ == '__main__':
    unittest.main()
