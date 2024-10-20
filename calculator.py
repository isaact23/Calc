import math
import re
import cmath
import unittest

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero."

def square(a):
    result = a * a
    if abs(result) == float('inf'):
        return "Error: Overflow occurred."
    return result

def power(a, n):
    try:
        result = a ** n
        if result == float('inf') or result == float('-inf'):
            return "Error: Overflow occurred."
        return result
    except OverflowError:
        return "Error: Overflow occurred."

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

# Define operator precedence
precedence = {
    '+': 1,
    '-': 1,
    '✕': 2,
    '➗': 2,
    'sin': 3,
    'cos': 3,
    'tan': 3,
    '√': 3,    # nth root
    '^': 3,    # Power
    '(': 0,
}

# Function to apply the operator to the values stack
def apply_operator(operators, values):
    operator = operators.pop()
    
    if operator == '+':
        values.append(values.pop() + values.pop())
    elif operator == '-':
        b = values.pop()
        a = values.pop()
        values.append(a - b)
    elif operator == '✕':
        values.append(values.pop() * values.pop())
    elif operator == '➗':
        b = values.pop()
        a = values.pop()
        if b == 0:
            values.append('undefined')
        else:
            values.append(a / b)
    elif operator == '^':
        b = values.pop()
        a = values.pop()
        values.append(a ** b)  # Using the built-in power operator
    elif operator == '√':  # nth root or square root
        a = values.pop()
        n = values.pop() if values else 2  # Default to square root if no explicit 'n'
        values.append(nth_root(a, n))  # Use the custom nth_root function
    # Handle trigonometric functions
    elif operator == 'sin':
        values.append(sin(values.pop()))  # Use the custom sin function
    elif operator == 'cos':
        values.append(cos(values.pop()))  # Use the custom cos function
    elif operator == 'tan':
        values.append(tan(values.pop()))  # Use the custom tan function

# Function to evaluate an expression
def evaluate_expression(expression):
    operators = []  # Stack for operators
    values = []     # Stack for values

    # Tokenize the input
    tokens = tokenize(expression)

    for token in tokens:
        if is_number(token):
            values.append(float(token))
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()  # Remove '(' from the stack
        elif token in precedence:
            while (operators and operators[-1] != '(' and 
                   precedence[operators[-1]] >= precedence[token]):
                apply_operator(operators, values)
            operators.append(token)

    # Apply remaining operators
    while operators:
        apply_operator(operators, values)

    return values[0]

# Helper function to check if a token is a number
def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

# Helper function to tokenize input, including handling nth roots and Unicode characters
def tokenize(expression):
    # Tokenize the input expression using regular expressions
    token_pattern = r'(\d+\.?\d*|[+\-✕➗\^√()]|sin|cos|tan|\d+√)'
    tokens = re.findall(token_pattern, expression)

    # Handle nth root like '3√' by splitting it into '3', '√'
    processed_tokens = []
    for token in tokens:
        if '√' in token and len(token) > 1:  # Handle nth roots like '3√'
            num_root, root_char = token[:-1], token[-1]
            processed_tokens.append(num_root)
            processed_tokens.append(root_char)
        else:
            processed_tokens.append(token)

    return processed_tokens

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

if __name__ == '__main__':
    unittest.main()