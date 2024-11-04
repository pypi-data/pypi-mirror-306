import unittest

class TestBasicOperations(unittest.TestCase):
    
    def test_addition(self):
        self.assertEqual(1 + 1, 2)
    
    def test_subtraction(self):
        self.assertEqual(2 - 1, 1)
    
    def test_multiplication(self):
        self.assertEqual(2 * 2, 4)
    
    def test_division(self):
        self.assertEqual(4 / 2, 2)

if __name__ == '__main__':
    unittest.main()