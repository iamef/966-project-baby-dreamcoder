import unittest
from primitives import *
from handcoded_to_learn import *
from wake import *


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


class TestWake(unittest.TestCase):
    def test_get_functions_by_types(self):
        int_inputs_actual = get_functions_by_types((int,), (int,))
        bool_inputs_actual = get_functions_by_types((bool,), (bool,))

        self.assertEqual()



if __name__ == '__main__':
    unittest.main()