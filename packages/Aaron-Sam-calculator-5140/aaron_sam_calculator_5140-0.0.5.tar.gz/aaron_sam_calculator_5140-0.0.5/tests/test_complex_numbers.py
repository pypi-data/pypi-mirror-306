#testing complex_numbers.py

import unittest

from calculator import complex_add, complex_subtract, complex_multiply, complex_divide

class TestComplexNumbers(unittest.TestCase):
    def test_complex_add(self):
        self.assertEqual(complex_add(1+4j, 4+3j), 5+7j)
        self.assertEqual(complex_add(0+0j, 0+0j), 0+0j)
        self.assertEqual(complex_add(-1-1j, -1-1j), -2-2j)
        self.assertEqual(complex_add(-1+1j, 1-1j), 0+0j)
    
    def test_complex_subtract(self):
        self.assertEqual(complex_subtract(1+4j, 4+3j), -3+1j)
        self.assertEqual(complex_subtract(0+0j, 0+0j), 0+0j)
        self.assertEqual(complex_subtract(-1-1j, -1-1j), 0+0j)
        self.assertEqual(complex_subtract(-1+1j, 1-1j), -2+2j)

    def test_complex_multiply(self):
        self.assertEqual(complex_multiply(1+4j, 4+3j), 1+16j)
        self.assertEqual(complex_multiply(0+0j, 0+0j), 0+0j)
        self.assertEqual(complex_multiply(-1-1j, -1-1j), 0+2j)
        self.assertEqual(complex_multiply(-1+1j, 1-1j), 0-2j)

    def test_complex_divide(self):
        self.assertEqual(complex_divide(1+4j, 4+3j), 0.52+0.76j)
        self.assertEqual(complex_divide(0+0j, 0+0j), 0+0j)
        self.assertEqual(complex_divide(-1-1j, -1-1j), 1+0j)
        self.assertEqual(complex_divide(-1+1j, 1-1j), 0-1j)

if __name__ == '__main__':
    unittest.main()