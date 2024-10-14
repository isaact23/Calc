# Collect ARGS

# Do stuff with branches

import math
import cmath

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
