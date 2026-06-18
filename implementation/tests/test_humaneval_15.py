
import unittest
from humaneval_15 import string_sequence

class TestStringSequence(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(string_sequence(0), "0")
    def test_positive(self):
        self.assertEqual(string_sequence(5), "0 1 2 3 4 5")
    def test_one(self):
        self.assertEqual(string_sequence(1), "0 1")
    def test_negative(self):
        # Assuming function should handle negative by returning empty string
        self.assertEqual(string_sequence(-1), "")
    def test_large(self):
        self.assertEqual(string_sequence(10), "0 1 2 3 4 5 6 7 8 9 10")

if __name__ == "__main__":
    unittest.main()
