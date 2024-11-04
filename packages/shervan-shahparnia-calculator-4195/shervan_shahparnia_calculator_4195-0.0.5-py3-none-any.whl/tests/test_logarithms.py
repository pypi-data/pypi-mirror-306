import unittest
import math

class TestLogarithms(unittest.TestCase):
    
    def test_log_base_10(self):
        self.assertAlmostEqual(math.log10(100), 2)
    
    def test_natural_log(self):
        self.assertAlmostEqual(math.log(math.e), 1)
    
    def test_log_base_2(self):
        self.assertAlmostEqual(math.log2(8), 3)

if __name__ == '__main__':
    unittest.main()