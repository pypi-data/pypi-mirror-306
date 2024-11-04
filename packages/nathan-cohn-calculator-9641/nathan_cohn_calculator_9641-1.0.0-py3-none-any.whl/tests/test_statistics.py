import unittest
from calculator.statistics import mean, median, mode, stddev
import statistics

class TestStatisticsCalculator(unittest.TestCase):

    def test_mean(self):
        self.assertAlmostEqual(mean([1, 2, 3, 4, 5]), 3.0)
        self.assertAlmostEqual(mean([1.5, 2.5, 3.5]), 2.5)
        with self.assertRaises(ValueError):
            mean([])

    def test_median(self):
        self.assertAlmostEqual(median([1, 3, 3, 6, 7, 8, 9]), 6)
        self.assertAlmostEqual(median([1, 2, 3, 4, 5]), 3)
        self.assertAlmostEqual(median([1, 2, 3, 4]), 2.5)
        with self.assertRaises(ValueError):
            median([])

    def test_mode(self):
        self.assertAlmostEqual(mode([1, 2, 2, 3, 4]), 2)
        self.assertAlmostEqual(mode([1, 1, 2, 3, 3, 3, 4]), 3)
        self.assertAlmostEqual(mode([1, 2, 3, 4, 5]), 1)
        with self.assertRaises(ValueError):
            mode([])

    def test_stddev(self):
        self.assertAlmostEqual(stddev([1, 2, 3, 4, 5]), 1.5811388300841898)
        self.assertAlmostEqual(stddev([1, 1, 1, 1, 1]), 0.0)
        with self.assertRaises(ValueError):
            stddev([1])
        with self.assertRaises(ValueError):
            stddev([])

if __name__ == '__main__':
    unittest.main()