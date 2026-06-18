
import unittest
from humaneval_11 import string_xor

class TestStringXor(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(string_xor('010', '110'), '100')
        self.assertEqual(string_xor('0', '0'), '0')
        self.assertEqual(string_xor('1', '0'), '1')
        self.assertEqual(string_xor('1010', '0101'), '1111')
    
    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            string_xor('01', '010')
    
    def test_invalid_characters(self):
        with self.assertRaises(ValueError):
            string_xor('02', '10')
        with self.assertRaises(ValueError):
            string_xor('10', '1a')
    
if __name__ == '__main__':
    unittest.main()
