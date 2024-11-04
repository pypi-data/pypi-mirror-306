import unittest
from calculator.complex_numbers import add, subtract, multiply, divide, conjugate

class TestComplexNumberOperations(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(1 + 2j, 3 + 4j), 4 + 6j)
        self.assertEqual(add(-1 - 2j, -3 - 4j), -4 - 6j)
        self.assertEqual(add(0 + 0j, 0 + 0j), 0 + 0j)

    def test_subtract(self):
        self.assertEqual(subtract(1 + 2j, 3 + 4j), -2 - 2j)
        self.assertEqual(subtract(-1 - 2j, -3 - 4j), 2 + 2j)
        self.assertEqual(subtract(0 + 0j, 0 + 0j), 0 + 0j)

    def test_multiply(self):
        self.assertEqual(multiply(1 + 2j, 3 + 4j), -5 + 10j)
        self.assertEqual(multiply(-1 - 2j, -3 - 4j), -5 + 10j)
        self.assertEqual(multiply(0 + 0j, 0 + 0j), 0 + 0j)

    def test_divide(self):
        self.assertEqual(divide(1 + 2j, 3 + 4j), (11/25) + (2/25j))
        self.assertEqual(divide(-1 - 2j, -3 - 4j), (11/25) + (2/25j))
        with self.assertRaises(ValueError):
            divide(1 + 2j, 0 + 0j)

    def test_conjugate(self):
        self.assertEqual(conjugate(1 + 2j), 1 - 2j)
        self.assertEqual(conjugate(-1 - 2j), -1 + 2j)
        self.assertEqual(conjugate(0 + 0j), 0 + 0j)

if __name__ == '__main__':
    unittest.main()