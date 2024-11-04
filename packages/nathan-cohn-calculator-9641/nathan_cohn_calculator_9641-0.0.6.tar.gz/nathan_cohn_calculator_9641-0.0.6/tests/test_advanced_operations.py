import unittest
from calculator.advanced_operations import AdvancedCalculator

class TestAdvancedOperations(unittest.TestCase):

    def test_power(self):
        self.assertEqual(AdvancedCalculator.power(2, 3), 8.0)
        self.assertEqual(AdvancedCalculator.power(5, 0), 1.0)
        self.assertEqual(AdvancedCalculator.power(2, -2), 0.25)
        self.assertAlmostEqual(AdvancedCalculator.power(2, 0.5), 1.41421356237)

    def test_sqrt(self):
        self.assertEqual(AdvancedCalculator.sqrt(16), 4.0)
        self.assertEqual(AdvancedCalculator.sqrt(0), 0.0)
        self.assertAlmostEqual(AdvancedCalculator.sqrt(2), 1.41421356237)
        with self.assertRaises(ValueError):
            AdvancedCalculator.sqrt(-1)

    def test_factorial(self):
        self.assertEqual(AdvancedCalculator.factorial(5), 120)
        self.assertEqual(AdvancedCalculator.factorial(0), 1)
        self.assertEqual(AdvancedCalculator.factorial(1), 1)
        with self.assertRaises(ValueError):
            AdvancedCalculator.factorial(-1)

if __name__ == '__main__':
    unittest.main()