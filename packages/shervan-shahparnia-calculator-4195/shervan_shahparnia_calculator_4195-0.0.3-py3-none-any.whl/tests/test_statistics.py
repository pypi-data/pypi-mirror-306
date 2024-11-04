import unittest
from statistics import mean, median, mode, standard_deviation

class TestStatisticsFunctions(unittest.TestCase):
    
    def test_mean(self):
        self.assertEqual(mean([1, 2, 3, 4, 5]), 3)
        self.assertEqual(mean([1, 1, 1, 1, 1]), 1)
        self.assertEqual(mean([1, 2, 3]), 2)
    
    def test_median(self):
        self.assertEqual(median([1, 2, 3, 4, 5]), 3)
        self.assertEqual(median([1, 2, 3, 4]), 2.5)
        self.assertEqual(median([3, 1, 2]), 2)
    
    def test_mode(self):
        self.assertEqual(mode([1, 1, 2, 2, 2, 3]), 2)
        self.assertEqual(mode([1, 1, 1, 2, 2, 3]), 1)
        self.assertEqual(mode([1, 2, 3, 4, 4, 4, 5, 5, 5, 5]), 5)
        self.assertEqual(mode([1, 2, 3]), "no unique mode; found 3 equally common values")
    
    def test_standard_deviation(self):
        self.assertAlmostEqual(standard_deviation([1, 2, 3, 4, 5]), 1.5811, places=4)
        self.assertAlmostEqual(standard_deviation([1, 1, 1, 1, 1]), 0)
        self.assertAlmostEqual(standard_deviation([1, 2, 3]), 1)

if __name__ == '__main__':
    unittest.main()