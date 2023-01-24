import unittest
from primitives import *
from handcoded_to_learn import *
from wake import *
from interpreter import *


class TestPrimitives(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(zero(), 0, "zero method should return 0")

    def test_pred(self):
        self.assertEqual(pred(5), 4, "pred of 5 should be 4")
        self.assertEqual(pred(1), 0, "pred of 1 should be 0")
        self.assertEqual(pred(0), -1, "pred of 0 should be -1")
        self.assertEqual(pred(-10), -11, "pred of -10 should be -11")

    def test_succ(self):
        self.assertEqual(succ(4), 5, "succ of 4 should be 5")
        self.assertEqual(succ(0), 1, "succ of 0 should be 1")
        self.assertEqual(succ(-1), 0, "succ of -1 should be 0")
        self.assertEqual(succ(-11), -10, "succ of -11 should be -10")

    def test_neg(self):
        self.assertEqual(neg(zero()), zero())
        self.assertEqual(neg(1), -1)
        self.assertEqual(neg(-9), 9)

    def test_equal(self):
        self.assertTrue(eq(zero(), 0), "eq(zero(), 0) should return true")
        self.assertTrue(eq(5, 5), "eq(5, 5) should return true")
        self.assertTrue(eq(-11, -11), "eq(-11, -11) should return true")
        self.assertFalse(eq(-10, 10), "eq(-10, 10) should return false")
        self.assertFalse(eq(5, 8), "eq(9, 8) should return false")

    def test_less_than(self):
        self.assertFalse(less_than(zero(), 0), "less_than(zero(), 0) should return false")
        self.assertTrue(less_than(-10, 10), "less_than(-10, 10) should return True")
        self.assertTrue(less_than(5, 8), "less_than(5, 8) should return True")
        self.assertFalse(less_than(11, 10), "less_than(11, 10) should return false")

    def test_conj(self):
        self.assertTrue(conj(True, True), "T and T should be T")
        self.assertFalse(conj(True, False))
        self.assertFalse(conj(False, True))
        self.assertFalse(conj(False, False))

    def test_disj(self):
        self.assertTrue(disj(True, True), "T and T should be T")
        self.assertTrue(disj(True, False))
        self.assertTrue(disj(False, True))
        self.assertFalse(disj(False, False))

    def test_cond(self):
        self.assertEqual(cond(True, zero(), succ(zero())), zero())
        self.assertEqual(cond(False, True, False), False)

    def test_ind(self):
        with self.assertRaises(ValueError):
            ind(zero(), pred(zero()), succ)
        self.assertEqual(ind(zero(), zero(), succ), 0)
        self.assertEqual(ind(zero(), succ(succ(succ(zero()))), succ), 3)
        self.assertEqual(ind(zero(), succ(succ(succ(succ(succ(zero()))))), pred), -5)


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
        zero_arg_prog = Program(zero, tuple())
        self.assertEqual(interpret(zero_arg_prog), 0)
        # one arg case
        one_arg_prog = Program(neg, (1,))
        self.assertEqual(interpret(one_arg_prog), -1)
        # two+ args case
        two_arg_prog = Program(less_than, (4, 5))
        self.assertEqual(interpret(two_arg_prog), True)
        three_arg_prog = Program(ind, (0, 5, pred))
        self.assertEqual(interpret(three_arg_prog), -5)
        positive_plus_prog = Program(ind, (5, 7, succ))
        self.assertEqual(interpret(positive_plus_prog), 12)

        # TWO LAYER CASES
        # one 2 layer, no other args
        just_two_layer_prog = Program(succ, (Program(succ, (7,)),))
        self.assertEqual(interpret(just_two_layer_prog), 9)
        # one 2 layers, one 1 layer
        two_layer_one_layer_prog = Program(eq, (
            -7,
            Program(neg, (7,))
        ))
        self.assertEqual(interpret(two_layer_one_layer_prog), True)

        # THREE or MORE LAYER CASES
        # one 6 layer case
        six_layer_prog = Program(
            pred, (
                Program(pred, (
                    Program(pred, (
                        Program(neg, (
                            Program(
                                succ, (Program(zero, tuple()),)
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

        plus_prog = Program(ind, (
            num1,
            Program(cond, (
                Program(less_than, (Program(zero, tuple()), num2)),
                num2,  # num2 positive case
                Program(neg, (num2,))  # num2 negative case TODO this is bad
            )),
            Program(cond, (
                Program(less_than, (Program(zero, tuple()), num2)),
                succ,  # num2 positive case
                pred  # num2 negative case
            ))
        ))

        self.assertEqual(interpret(plus_prog), -17)


class TestWake(unittest.TestCase):
    def test_get_functions_by_types(self):
        self.assertEqual(1, 1)
        int_inputs_actual = get_functions_by_types((int,), int)
        bool_inputs_actual = get_functions_by_types((bool,), bool)

    def test_generate_function(self):
        first_input_problem = Problem(
            input_type=(int, int, int, int, int),
            output_type=int,
            input_ouput_pairs=[
                ((42356, 1435, 123, 5, 176), 42356),
                ((1354, 2867, 1342, 814, 132), 1354),
                ((4, 2, 8, 3, 1), 4),
                ((89, 26, 27, 83, 34), 89),
                ((247, 56, 92, 74, 63), 247)
            ]
        )

        out_func = generate_function(first_input_problem)

        for inp, out in first_input_problem.input_ouput_pairs:
            actual_res: int = out_func(inp)
            print(actual_res == out, actual_res, out)

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


if __name__ == '__main__':
    unittest.main()
