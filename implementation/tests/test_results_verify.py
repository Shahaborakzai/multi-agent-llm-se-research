
import unittest
from humaneval_results.humaneval_0 import has_close_elements
from humaneval_results.humaneval_1 import separate_paren_groups

class TestHasCloseElements(unittest.TestCase):
    # Basic functionality tests
    def test_no_close_elements(self):
        self.assertFalse(has_close_elements([1.0, 2.0, 3.0], 0.5))

    def test_has_close_elements(self):
        self.assertTrue(has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3))

    # Edge case: empty list
    def test_empty_list(self):
        self.assertFalse(has_close_elements([], 1.0))

    # Edge case: single element
    def test_single_element(self):
        self.assertFalse(has_close_elements([1.0], 0.5))

    # Edge case: non‑positive threshold
    def test_nonpositive_threshold(self):
        self.assertFalse(has_close_elements([1.0, 1.1], 0.0))
        self.assertFalse(has_close_elements([1.0, 1.1], -1.0))

class TestSeparateParenGroups(unittest.TestCase):
    # Basic functionality tests
    def test_single_group(self):
        self.assertEqual(separate_paren_groups("(a)"), ["(a)"])

    def test_multiple_groups(self):
        self.assertEqual(separate_paren_groups("(a)(b)(c)"), ["(a)", "(b)", "(c)"])

    def test_nested_groups(self):
        self.assertEqual(separate_paren_groups("((a)(b))"), ["((a)(b))"])

    # Edge case: spaces ignored
    def test_spaces_ignored(self):
        self.assertEqual(separate_paren_groups("( a ) ( b )"), ["(a)", "(b)"])

    # Edge case: empty string
    def test_empty_string(self):
        self.assertEqual(separate_paren_groups(""), [])

    # Edge case: unbalanced input (should return groups formed before imbalance)
    def test_unbalanced_input(self):
        self.assertEqual(separate_paren_groups("(a)(b"), ["(a)"])

if __name__ == "__main__":
    unittest.main()
