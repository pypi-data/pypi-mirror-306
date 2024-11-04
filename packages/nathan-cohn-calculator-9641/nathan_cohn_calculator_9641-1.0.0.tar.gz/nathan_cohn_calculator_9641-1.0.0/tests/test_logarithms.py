import unittest
import math
from calculator.logarithms import log, ln, exp

class TestLogarithms(unittest.TestCase):

    def test_log(self):
        self.assertAlmostEqual(log(100, 10), 2.0)
        self.assertAlmostEqual(log(8, 2), 3.0)

    def test_log_invalid_x(self):
        with self.assertRaises(ValueError):
            log(-1, 10)

    def test_log_invalid_base(self):
        with self.assertRaises(ValueError):
            log(100, -10)

    def test_ln(self):
        self.assertAlmostEqual(ln(2.71828), 1.0, places=2)

    def test_ln_invalid_x(self):
        with self.assertRaises(ValueError):
            ln(-1)

    def test_exp(self):
        self.assertAlmostEqual(exp(1), 2.718281828459045)
        self.assertAlmostEqual(exp(0), 1.0)
        self.assertAlmostEqual(exp(-1), 1 / math.e)

    def test_additional_cases(self):
        self.assertAlmostEqual(log(25, 5), 2.0)
        self.assertAlmostEqual(log(math.e, math.e), 1.0)
        self.assertAlmostEqual(ln(1000000), 13.815510557964274)

if __name__ == '__main__':
    unittest.main()
