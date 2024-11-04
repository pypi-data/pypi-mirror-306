import unittest
from calculator.advanced_operations import power, sqrt, factorial

class TestAdvancedOperations(unittest.TestCase):

    def test_power(self):
        self.assertEqual(power(2, 3), 8.0)
        self.assertEqual(power(5, 0), 1.0)
        self.assertEqual(power(2, -2), 0.25)
        self.assertAlmostEqual(power(2, 0.5), 1.41421356237)

    def test_sqrt(self):
        self.assertEqual(sqrt(16), 4.0)
        self.assertEqual(sqrt(0), 0.0)
        self.assertAlmostEqual(sqrt(2), 1.41421356237)
        with self.assertRaises(ValueError):
            sqrt(-1)

    def test_factorial(self):
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        with self.assertRaises(ValueError):
            factorial(-1)
            
if __name__ == '__main__':
    unittest.main()
