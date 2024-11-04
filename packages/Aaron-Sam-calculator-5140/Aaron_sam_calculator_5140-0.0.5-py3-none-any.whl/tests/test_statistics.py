#testing statistics.py

import unittest
from statistics import mean, median, mode

class TestStatistics(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(mean([1, 2, 3, 4, 5]), 3)
        self.assertEqual(mean([1, 2, 3, 4]), 2.5)
        self.assertEqual(mean([1, 2, 3, 4, 5, 6]), 3.5)
        self.assertEqual(mean([1, 2, 3, 4, 5, 6, 7]), 4)

    def test_median(self):
        self.assertEqual(median([1, 2, 3, 4, 5]), 3)
        self.assertEqual(median([1, 2, 3, 4]), 2.5)
        self.assertEqual(median([1, 2, 3, 4, 5, 6]), 3.5)
        self.assertEqual(median([1, 2, 3, 4, 5, 6, 7]), 4)

    def test_mode(self):
        self.assertEqual(mode([1, 2, 3, 4, 5]), 1)
        self.assertEqual(mode([1, 2, 3, 4, 5, 1]), 1)
        self.assertEqual(mode([1, 2, 3, 4, 5, 1, 2]), 1)
        self.assertEqual(mode([1, 2, 3, 4, 5, 1, 2, 3]), 1)

if __name__ == '__main__':
    unittest.main()