
import unittest
import calculator

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calculator.add(2, 3), 5)
        self.assertEqual(calculator.add(-1, 1), 0)

    def test_sub(self):
        self.assertEqual(calculator.sub(5, 3), 2)
        self.assertEqual(calculator.sub(0, 5), -5)

    def test_mul(self):
        self.assertEqual(calculator.mul(4, 3), 12)
        self.assertEqual(calculator.mul(-2, 3), -6)

    def test_div(self):
        self.assertEqual(calculator.div(10, 2), 5)
        self.assertAlmostEqual(calculator.div(7, 3), 7/3)

    def test_div_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculator.div(5, 0)

if __name__ == '__main__':
    unittest.main()
