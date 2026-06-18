
import unittest
from humaneval_13 import greatest_common_divisor

class TestGreatestCommonDivisor(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(greatest_common_divisor(3, 5), 1)
        self.assertEqual(greatest_common_divisor(25, 15), 5)

    def test_zero(self):
        self.assertEqual(greatest_common_divisor(0, 5), 5)
        self.assertEqual(greatest_common_divisor(7, 0), 7)
        self.assertEqual(greatest_common_divisor(0, 0), 0)

    def test_negative(self):
        self.assertEqual(greatest_common_divisor(-12, 18), 6)
        self.assertEqual(greatest_common_divisor(-7, -14), 7)

    def test_random(self):
        self.assertEqual(greatest_common_divisor(48, 180), 12)
        self.assertEqual(greatest_common_divisor(101, 103), 1)

if __name__ == '__main__':
    unittest.main()
