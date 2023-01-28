import unittest
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
    def test_get_functions_by_types(self):
        self.assertEqual(1, 1)
        int_inputs_actual = get_functions_by_types((int,), int)
        bool_inputs_actual = get_functions_by_types((bool,), bool)

    def test_get_all_function_specific_fillings(self):
        funcs = get_functions_by_output_type(int)

        for func in funcs:
            get_all_function_specific_fillings(func, {int: ["x_0", "x_1", "x_3"], bool: ["x_2"]}, {})

    def test_get_all_overall_fillings(self):
        func_comp = [
            primi.cond,
            [primi.less_than, primi.succ, primi.pred],
            [[primi.succ, primi.pred], [primi.zero], [primi.pred]]
        ]

        get_all_overall_fillings(func_comp, {int: ["x_0", "x_1", "x_3"], bool: ["x_2"]}, {})


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

        for out_prog in out_progs:
            for inp, out in first_input_problem.input_ouput_pairs:
                actual_res: int = interpret(out_prog, inp)
                print(actual_res == out, actual_res, out)

        everything_zero_problem = Problem(
            input_type=(Any,),
            output_type=int,
            input_ouput_pairs=[
                (True, 0),
                ([1, 2, 3], 0),
                (134, 0),
                (-1530, 0),
                ((False, True), 0)
            ]
        )
        # actually

        out_progs = generate_programs(everything_zero_problem)

        for out_prog in out_progs:
            for inp, out in everything_zero_problem.input_ouput_pairs:
                actual_res: int = interpret(out_prog, inp)
                print(actual_res == out, actual_res, out)


if __name__ == '__main__':
    unittest.main()
