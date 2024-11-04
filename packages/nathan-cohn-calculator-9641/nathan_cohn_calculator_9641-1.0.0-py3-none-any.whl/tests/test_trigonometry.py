import unittest
import math
from calculator.trigonometry import sin, cos, tan

class TestTrigonometryFunctions(unittest.TestCase):

    def test_sin(self):
        self.assertAlmostEqual(sin(math.pi / 2), 1.0)
        self.assertAlmostEqual(sin(0), 0.0)
        self.assertAlmostEqual(sin(math.pi), 0.0)
        self.assertAlmostEqual(sin(3 * math.pi / 2), -1.0)
        self.assertAlmostEqual(sin(math.pi / 6), 0.5)

    def test_cos(self):
        self.assertAlmostEqual(cos(math.pi), -1.0)
        self.assertAlmostEqual(cos(0), 1.0)
        self.assertAlmostEqual(cos(math.pi / 2), 0.0)
        self.assertAlmostEqual(cos(3 * math.pi / 2), 0.0)
        self.assertAlmostEqual(cos(math.pi / 3), 0.5)

    def test_tan(self):
        self.assertAlmostEqual(tan(math.pi / 4), 1.0)
        self.assertAlmostEqual(tan(0), 0.0)
        self.assertAlmostEqual(tan(math.pi), 0.0)
        self.assertAlmostEqual(tan(math.pi / 6), math.sqrt(3) / 3)
        with self.assertRaises(ValueError):
            tan(math.pi / 2)
        with self.assertRaises(ValueError):
            tan(3 * math.pi / 2)

if __name__ == '__main__':
    unittest.main()