
import unittest
from humaneval_14 import all_prefixes

class TestAllPrefixes(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(all_prefixes('abc'), ['a', 'ab', 'abc'])
        self.assertEqual(all_prefixes(''), [])
        self.assertEqual(all_prefixes('a'), ['a'])
        self.assertEqual(all_prefixes('ab'), ['a', 'ab'])
        self.assertEqual(all_prefixes('hello'), ['h', 'he', 'hel', 'hell', 'hello'])

    def test_long_string(self):
        s = 'abcdefghij'
        expected = [s[:i] for i in range(1, len(s)+1)]
        self.assertEqual(all_prefixes(s), expected)

if __name__ == '__main__':
    unittest.main()
