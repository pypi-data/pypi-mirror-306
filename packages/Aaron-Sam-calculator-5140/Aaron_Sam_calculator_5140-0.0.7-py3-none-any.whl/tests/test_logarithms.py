#testing logarithms.py

import unittest

from calculator.logarithms import log, ln, exponential

class TestLogarithms(unittest.TestCase):
    def test_log(self):
        self.assertEqual(log(10), 2.302585092994046)
        self.assertEqual(log(1), 0)
        self.assertEqual(log(2), 0.6931471805599453)
        self.assertEqual(log(4), 1.3862943611198906)

    def test_ln(self):
        self.assertEqual(ln(10), 2.302585092994046)
        self.assertEqual(ln(1), 0)
        self.assertEqual(ln(2), 0.6931471805599453)
        self.assertEqual(ln(4), 1.3862943611198906)

    def test_exponential(self):
        self.assertEqual(exponential(10), 22026.465794806718)
        self.assertEqual(exponential(1), 2.718281828459045)
        self.assertEqual(exponential(2), 7.38905609893065)
        self.assertEqual(exponential(4), 54.598150033144236)