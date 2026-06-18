
import unittest
from humaneval_10 import is_palindrome

class TestIsPalindrome(unittest.TestCase):
    def test_empty(self):
        self.assertTrue(is_palindrome(''))

    def test_true_cases(self):
        self.assertTrue(is_palindrome('a'))
        self.assertTrue(is_palindrome('aba'))
        self.assertTrue(is_palindrome('abba'))
        self.assertTrue(is_palindrome('madam'))

    def test_false_cases(self):
        self.assertFalse(is_palindrome('ab'))
        self.assertFalse(is_palindrome('abc'))
        self.assertFalse(is_palindrome('abaa'))
        self.assertFalse(is_palindrome('hello'))

if __name__ == '__main__':
    unittest.main()
