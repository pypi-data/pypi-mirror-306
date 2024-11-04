import unittest
from calculator.basic_operations import Calculator

class TestBasicOperations(unittest.TestCase):

    def test_add(self):
        self.assertEqual(Calculator.add(3, 5), 8.0)
        self.assertEqual(Calculator.add(-1, 1), 0.0)
        self.assertEqual(Calculator.add(-1, -1), -2.0)
        self.assertEqual(Calculator.add(0, 0), 0.0)

    def test_subtract(self):
        self.assertEqual(Calculator.subtract(10, 5), 5.0)
        self.assertEqual(Calculator.subtract(-1, 1), -2.0)
        self.assertEqual(Calculator.subtract(-1, -1), 0.0)
        self.assertEqual(Calculator.subtract(0, 0), 0.0)

    def test_multiply(self):
        self.assertEqual(Calculator.multiply(4, 5), 20.0)
        self.assertEqual(Calculator.multiply(-1, 1), -1.0)
        self.assertEqual(Calculator.multiply(-1, -1), 1.0)
        self.assertEqual(Calculator.multiply(0, 5), 0.0)

    def test_divide(self):
        self.assertEqual(Calculator.divide(10, 2), 5.0)
        self.assertEqual(Calculator.divide(-1, 1), -1.0)
        self.assertEqual(Calculator.divide(-1, -1), 1.0)
        self.assertEqual(Calculator.divide(0, 1), 0.0)
        with self.assertRaises(ValueError):
            Calculator.divide(10, 0)

if __name__ == '__main__':
    unittest.main()