import unittest
from calculator.complex_numbers import add_complex, subtract_complex, multiply_complex, divide_complex, conjugate

class TestComplexNumbers(unittest.TestCase):

    def test_add_complex(self):
        self.assertEqual(add_complex(1+2j, 3+4j), 4+6j)
        self.assertEqual(add_complex(-1-2j, -3-4j), -4-6j)
        self.assertEqual(add_complex(0, 0), 0)

    def test_subtract_complex(self):
        self.assertEqual(subtract_complex(1+2j, 3+4j), -2-2j)
        self.assertEqual(subtract_complex(-1-2j, -3-4j), 2+2j)
        self.assertEqual(subtract_complex(0, 0), 0)

    def test_multiply_complex(self):
        self.assertEqual(multiply_complex(1+2j, 3+4j), -5+10j)
        self.assertEqual(multiply_complex(-1-2j, -3-4j), -5-10j)
        self.assertEqual(multiply_complex(0, 1+1j), 0)

    def test_divide_complex(self):
        self.assertEqual(divide_complex(1+2j, 3+4j), 0.44+0.08j)
        self.assertEqual(divide_complex(-1-2j, -3-4j), 0.44+0.08j)
        self.assertEqual(divide_complex(0, 1+1j), 0)
        self.assertEqual(divide_complex(1+1j, 0), "Error: Division by zero")

    def test_conjugate(self):
        self.assertEqual(conjugate(1+2j), 1-2j)
        self.assertEqual(conjugate(-1-2j), -1+2j)
        self.assertEqual(conjugate(0), 0)

if __name__ == '__main__':
    unittest.main()