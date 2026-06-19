
import unittest
from math_utils import is_prime, factorial, fibonacci

class TestMathUtils(unittest.TestCase):
    # is_prime tests
    def test_is_prime_basic(self):
        self.assertFalse(is_prime(-5))
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertFalse(is_prime(4))
        self.assertTrue(is_prime(13))
        self.assertFalse(is_prime(100))

    def test_is_prime_large(self):
        # 104729 is the 10000th prime
        self.assertTrue(is_prime(104729))

    # factorial tests
    def test_factorial_edge(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)

    def test_factorial_negative(self):
        with self.assertRaises(ValueError):
            factorial(-3)

    def test_factorial_large(self):
        # 10! = 3628800
        self.assertEqual(factorial(10), 3628800)

    # fibonacci tests
    def test_fibonacci_edge(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(3), 2)
        self.assertEqual(fibonacci(10), 55)

    def test_fibonacci_negative(self):
        with self.assertRaises(ValueError):
            fibonacci(-1)

    def test_fibonacci_large(self):
        # 20th Fibonacci number is 6765
        self.assertEqual(fibonacci(20), 6765)

if __name__ == "__main__":
    unittest.main()
