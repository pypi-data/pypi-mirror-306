#testing advanced_operations.py

import unittest

from calculator import power, sqrt

class TestAdvancedOperations(unittest.TestCase):
    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(0, 0), 1)
        self.assertEqual(power(-1, 2), 1)
        self.assertEqual(power(2, -1), 0.5)

    def test_sqrt(self):
        self.assertEqual(sqrt(9), 3)
        self.assertEqual(sqrt(0), 0)
        self.assertEqual(sqrt(-1), 0)

if __name__ == '__main__':
    unittest.main()