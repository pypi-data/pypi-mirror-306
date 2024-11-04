import unittest
import math
from calculator.trigonometry import TrigonometryCalculator

class TestTrigonometryCalculator(unittest.TestCase):

    def test_sin(self):
        self.assertAlmostEqual(TrigonometryCalculator.sin(math.pi / 2), 1.0)
        self.assertAlmostEqual(TrigonometryCalculator.sin(0), 0.0)
        self.assertAlmostEqual(TrigonometryCalculator.sin(math.pi), 0.0)
        self.assertAlmostEqual(TrigonometryCalculator.sin(3 * math.pi / 2), -1.0)

    def test_cos(self):
        self.assertAlmostEqual(TrigonometryCalculator.cos(math.pi), -1.0)
        self.assertAlmostEqual(TrigonometryCalculator.cos(0), 1.0)
        self.assertAlmostEqual(TrigonometryCalculator.cos(math.pi / 2), 0.0)
        self.assertAlmostEqual(TrigonometryCalculator.cos(3 * math.pi / 2), 0.0)

    def test_tan(self):
        self.assertAlmostEqual(TrigonometryCalculator.tan(math.pi / 4), 1.0)
        self.assertAlmostEqual(TrigonometryCalculator.tan(0), 0.0)
        self.assertAlmostEqual(TrigonometryCalculator.tan(math.pi), 0.0)
        with self.assertRaises(ValueError):
            TrigonometryCalculator.tan(math.pi / 2)
        with self.assertRaises(ValueError):
            TrigonometryCalculator.tan(3 * math.pi / 2)

if __name__ == '__main__':
    unittest.main()