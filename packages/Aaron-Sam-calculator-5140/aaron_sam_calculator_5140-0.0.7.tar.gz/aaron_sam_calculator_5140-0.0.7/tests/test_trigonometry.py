#testing trigonometry.py

import unittest
from calculator.trigonometry import sin, cos, tan

class TestTrigonometry(unittest.TestCase):
    def test_sin(self):
        self.assertEqual(sin(0), 0)
        self.assertEqual(sin(30), 0.5)
        self.assertEqual(sin(45), 0.7071067811865475)
        self.assertEqual(sin(60), 0.8660254037844386)
        self.assertEqual(sin(90), 1)
    
    def test_cos(self):
        self.assertEqual(cos(0), 1)
        self.assertEqual(cos(30), 0.8660254037844387)
        self.assertEqual(cos(45), 0.7071067811865476)
        self.assertEqual(cos(60), 0.5)
        self.assertEqual(cos(90), 6.123233995736766e-17)
    
    def test_tan(self):
        self.assertEqual(tan(0), 0)
        self.assertEqual(tan(30), 0.5773502691896257)
        self.assertEqual(tan(45), 1.0)
        self.assertEqual(tan(60), 1.7320508075688772)
        self.assertEqual(tan(90), 1.633123935319537e+16)