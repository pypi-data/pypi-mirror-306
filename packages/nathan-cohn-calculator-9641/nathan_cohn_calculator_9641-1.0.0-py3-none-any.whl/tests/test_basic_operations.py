import unittest
from calculator.basic_operations import add, subtract, multiply, divide

class TestBasicOperations(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(3, 5), 8.0)
        self.assertEqual(add(-1, 1), 0.0)
        self.assertEqual(add(-1, -1), -2.0)
        self.assertEqual(add(0, 0), 0.0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5.0)
        self.assertEqual(subtract(-1, 1), -2.0)
        self.assertEqual(subtract(-1, -1), 0.0)
        self.assertEqual(subtract(0, 0), 0.0)

    def test_multiply(self):
        self.assertEqual(multiply(4, 5), 20.0)
        self.assertEqual(multiply(-1, 1), -1.0)
        self.assertEqual(multiply(-1, -1), 1.0)
        self.assertEqual(multiply(0, 5), 0.0)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5.0)
        self.assertEqual(divide(-1, 1), -1.0)
        self.assertEqual(divide(-1, -1), 1.0)
        self.assertEqual(divide(0, 1), 0.0)
        with self.assertRaises(ValueError):
            divide(10, 0)

if __name__ == '__main__':
    unittest.main()