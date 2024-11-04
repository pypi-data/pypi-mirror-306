import unittest
import math
from calculator.trigonometry import sine, cosine, tangent

class TestTrigonometry(unittest.TestCase):
        
    def test_sine(self):
        self.assertAlmostEqual(sine(90), 1)
        self.assertAlmostEqual(sine(0), 0)
        self.assertAlmostEqual(sine(30), 0.5)
        self.assertAlmostEqual(sine(45), math.sqrt(2) / 2)
        
    def test_cosine(self):
        self.assertAlmostEqual(cosine(0), 1)
        self.assertAlmostEqual(cosine(60), 0.5)
        self.assertAlmostEqual(cosine(90), 0)
        self.assertAlmostEqual(cosine(45), math.sqrt(2) / 2)
        
    def test_tangent(self):
        self.assertAlmostEqual(tangent(45), 1)
        self.assertAlmostEqual(tangent(0), 0)
        self.assertAlmostEqual(tangent(30), math.sqrt(3) / 3)
        self.assertAlmostEqual(tangent(60), math.sqrt(3))

if __name__ == '__main__':
        unittest.main()
