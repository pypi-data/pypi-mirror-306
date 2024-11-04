import unittest
from calculator.logarithms import ExponentialCalculator

class TestLogarithms(unittest.TestCase):

    def test_log_base_10(self):
        self.assertAlmostEqual(ExponentialCalculator.log(100, 10), 2.0)

    def test_log_base_2(self):
        self.assertAlmostEqual(ExponentialCalculator.log(8, 2), 3.0)

    def test_log_invalid_x(self):
        with self.assertRaises(ValueError):
            ExponentialCalculator.log(-1, 10)

    def test_log_invalid_base(self):
        with self.assertRaises(ValueError):
            ExponentialCalculator.log(100, -10)

    def test_ln(self):
        self.assertAlmostEqual(ExponentialCalculator.ln(2.71828), 1.0, places=2)

    def test_ln_invalid_x(self):
        with self.assertRaises(ValueError):
            ExponentialCalculator.ln(-1)

    def test_exp(self):
        self.assertAlmostEqual(ExponentialCalculator.exp(1), 2.718281828459045)

if __name__ == '__main__':
    unittest.main()