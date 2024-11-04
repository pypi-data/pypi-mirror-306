import unittest
from calculator.statistics import StatisticsCalculator
import statistics

class TestStatisticsCalculator(unittest.TestCase):

    def test_mean(self):
        self.assertAlmostEqual(StatisticsCalculator.mean([1, 2, 3, 4, 5]), 3.0)
        self.assertAlmostEqual(StatisticsCalculator.mean([1.5, 2.5, 3.5]), 2.5)
        with self.assertRaises(ValueError):
            StatisticsCalculator.mean([])

    def test_median(self):
        self.assertAlmostEqual(StatisticsCalculator.median([1, 3, 3, 6, 7, 8, 9]), 6)
        self.assertAlmostEqual(StatisticsCalculator.median([1, 2, 3, 4, 5]), 3)
        self.assertAlmostEqual(StatisticsCalculator.median([1, 2, 3, 4]), 2.5)
        with self.assertRaises(ValueError):
            StatisticsCalculator.median([])

    def test_mode(self):
        self.assertAlmostEqual(StatisticsCalculator.mode([1, 2, 2, 3, 4]), 2)
        self.assertAlmostEqual(StatisticsCalculator.mode([1, 1, 2, 3, 3, 3, 4]), 3)
        with self.assertRaises(ValueError):
            StatisticsCalculator.mode([])
        with self.assertRaises(statistics.StatisticsError):
            StatisticsCalculator.mode([1, 2, 3, 4, 5])  # No unique mode

    def test_stddev(self):
        self.assertAlmostEqual(StatisticsCalculator.stddev([1, 2, 3, 4, 5]), 1.5811388300841898)
        self.assertAlmostEqual(StatisticsCalculator.stddev([1, 1, 1, 1, 1]), 0.0)
        with self.assertRaises(ValueError):
            StatisticsCalculator.stddev([1])
        with self.assertRaises(ValueError):
            StatisticsCalculator.stddev([])

if __name__ == '__main__':
    unittest.main()