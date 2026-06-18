
import unittest
from humaneval_8 import sum_product

class TestSumProduct(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(sum_product([1, 2, 3, 4]), (10, 24))
        self.assertEqual(sum_product([]), (0, 1))
        self.assertEqual(sum_product([5]), (5, 5))
        self.assertEqual(sum_product([-1, 2, -3]), (-2, 6))

    def test_large_numbers(self):
        self.assertEqual(sum_product([10, 20, 30]), (60, 6000))

if __name__ == "__main__":
    unittest.main()
