
import unittest
from humaneval_6 import parse_nested_parens

class TestParseNestedParens(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(
            parse_nested_parens('(()()) ((())) () ((())()())'),
            [2, 3, 1, 3]
        )
    def test_empty(self):
        self.assertEqual(parse_nested_parens(''), [])
    def test_single_group(self):
        self.assertEqual(parse_nested_parens('((()))'), [3])
    def test_multiple_spaces(self):
        self.assertEqual(parse_nested_parens('()   (())   ((()))'), [1, 2, 3])
    def test_unbalanced(self):
        # Function assumes well‑formed input; unbalanced parentheses will be ignored for depth
        self.assertEqual(parse_nested_parens('(()'), [2])
        self.assertEqual(parse_nested_parens('())'), [1])

if __name__ == '__main__':
    unittest.main()
