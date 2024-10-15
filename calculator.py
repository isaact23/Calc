# Collect ARGS

# Do stuff with branches

import math
import cmath
import unittest

def sin(x):
    """
    Calculate the sine of x (in radians).
    """
    return math.sin(x)

def cos(x):
    """
    Calculate the cosine of x (in radians).
    """
    return math.cos(x)

def tan(x):
    """
    Calculate the tangent of x (in radians).
    Raises ValueError for x values that result in undefined tangent.
    """
    if abs(cos(x)) < 1e-15:  # Close to zero
        raise ValueError("Tangent is undefined for this input.")
    return math.tan(x)

def square_root(x):
    """
    Calculate the square root of x.
    Returns a complex number if x is negative.
    """
    if x < 0:
        return cmath.sqrt(x)
    return math.sqrt(x)

def nth_root(x, n):
    """
    Calculate the nth root of x.
    Raises ValueError for even roots of negative numbers.
    Returns a complex number for odd roots of negative numbers.
    """
    if x < 0:
        if n % 2 == 0:
            raise ValueError("Even root of a negative number is undefined in the real domain.")
        else:
            return -(-x) ** (1/n)
    return x ** (1/n)

class TestTrigAndRootFunctions(unittest.TestCase):

    # Trigonometric Function Tests
    def test_sin(self):
        self.assertAlmostEqual(sin(math.pi / 2), 1, places=5)
        self.assertAlmostEqual(sin(0), 0, places=5)
        self.assertAlmostEqual(sin(math.pi), 0, places=5)

    def test_cos(self):
        self.assertAlmostEqual(cos(math.pi), -1, places=5)
        self.assertAlmostEqual(cos(0), 1, places=5)
        self.assertAlmostEqual(cos(math.pi / 2), 0, places=5)

    def test_tan(self):
        self.assertAlmostEqual(tan(0), 0, places=5)
        self.assertAlmostEqual(tan(math.pi / 4), 1, places=5)
        with self.assertRaises(ValueError):  # Test for undefined tangent
            tan(math.pi / 2)

    # Root Function Tests
    def test_square_root(self):
        self.assertEqual(square_root(16), 4)
        self.assertEqual(square_root(0), 0)
        self.assertAlmostEqual(square_root(-4), cmath.sqrt(-4))
        result = square_root(-4)
        self.assertAlmostEqual(result.real, 0)
        self.assertAlmostEqual(result.imag, 2)

    def test_nth_root(self):
        self.assertEqual(nth_root(27, 3), 3)      # Cube root of 27
        self.assertEqual(nth_root(16, 4), 2)      # Fourth root of 16
        self.assertAlmostEqual(nth_root(-27, 3), -3)  # Cube root of -27
        self.assertAlmostEqual(nth_root(8, 1.5), 4)   # Non-integer root test
        self.assertAlmostEqual(nth_root(1e9, 3), 1000) # Large exponent test
        with self.assertRaises(ValueError):       # Test for even root of negative
            nth_root(-16, 2)
    
    def test_nth_root_complex(self):
        result = nth_root(-8, 3)
        self.assertAlmostEqual(result, -2)   # Test for negative number with odd root