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
        return None


def square(a):
    result = a * a
    if abs(result) == float("inf"):
        return None
    return result


def power(a, n):
    try:
        result = a**n
        if isinstance(result, complex):
            return None
        return result
    except:
        return None

def sin(x):
    return math.sin(x)


def cos(x):
    return math.cos(x)


def tan(x):
    if abs(cos(x)) < 1e-15:  # Check for undefined tangent
        return None
    return math.tan(x)


def nth_root(x, n):
    if x < 0 and n % 2 == 0:
        # Even root of a negative number should return None (undefined)
        return None
    elif x < 0 and n % 2 != 0:
        # For odd roots of negative numbers, return the negative of the root of the absolute value
        return -(-x) ** (1 / n)
    else:
        # For positive numbers or zero
        result = x ** (1 / n)
        return result if not isinstance(result, complex) else None


def square_root(x):
    return nth_root(x, 2)

# Define operator precedence
def apply_operator(operators, values):
    if not operators or len(values) < 1:
        return
        
    operator = operators.pop()
    
    if operator in ["+", "-"]:
        b = values.pop()
        if len(values) == 0:
            values.append(-b if operator == "-" else b)
        else:
            a = values.pop()
            values.append(add(a, b) if operator == "+" else subtract(a, b))
    
    elif operator in ["*", "✕"]:
        if len(values) < 2:
            return
        b = values.pop()
        a = values.pop()

        values.append(multiply(a, b))
    
    elif operator in ["/", "➗"]:
        if len(values) < 2:
            return
        b = values.pop()
        a = values.pop()

        values.append(divide(a, b))

    elif operator == "^":
        if len(values) < 2:
            return
        b = values.pop()
        a = values.pop()
        values.append(power(a, b))
    
    elif operator == "√":
        if len(values) < 1:
            return
        x = values.pop()
        n = values.pop() if values and isinstance(values[-1], (int, float)) else 2
        
        if (n % 2 == 0 and x < 0) or x is None:
            values.append(None)
        else:
            if x < 0:
                values.append(None)
            else:
                values.append(nth_root(x, n))
    
    elif operator in ["sin", "cos", "tan"]:
        if len(values) < 1:
            return
        x = values.pop()
        if operator == "sin":
            values.append(sin(x))
        elif operator == "cos":
            values.append(cos(x))
        else:  # tan
            if abs(cos(x)) < 1e-10:
                values.append(None)
            else:
                values.append(tan(x))


def normalize_expression(expression):
    """Fix garbled symbols and normalize the expression."""
    replacements = {
        'âž—': '/',  # Garbled division symbol
        'âœ•': '*',  # Garbled multiplication symbol
        '➗': '/',    # Division symbol
        'âˆš': '√',  # Garbled square root symbol
        'Ã·': '/',   # Garbled division symbol
        'âˆ': '-',   # Garbled negative sign
        '√': '√',    # Square root symbol
        '✕': '*',    # Multiplication symbol
    }
    for garbled, correct in replacements.items():
        expression = expression.replace(garbled, correct)
    return expression


def tokenize(expression):
    # Normalize the expression to replace garbled symbols
    expression = normalize_expression(expression)
    
    # Handle spaces and implicit multiplication
    expression = re.sub(r'\)\s*\(', ')*(', expression)  # Handle implicit multiplication: ")("
    expression = re.sub(r'(\d+|\))\s*\(', r'\1*(', expression)  # Handle cases like "2(" as "2*("
    expression = re.sub(r'\s*\(\s*', '(', expression)
    expression = re.sub(r'\s*\)\s*', ')', expression)
    expression = re.sub(r'(\d+|\))\s*\(', r'\1*(', expression)
    expression = re.sub(r'(sin|cos|tan)\s*\(', r'\1(', expression)
    
    tokens = []
    i = 0
    length = len(expression)
    
    while i < length:
        char = expression[i]
        
        if char.isspace():
            i += 1
            continue
            
        # Handle numbers (including negative numbers)
        if char.isdigit() or char == '.' or (char == '-' and 
           (i == 0 or expression[i-1] in '(+-*/^√')):
            number = char
            i += 1
            while i < length and (expression[i].isdigit() or expression[i] == '.'):
                number += expression[i]
                i += 1
            tokens.append(number)
            continue
            
        # Handle functions
        if i + 2 < length and expression[i:i+3] in ['sin', 'cos', 'tan']:
            tokens.append(expression[i:i+3])
            i += 3
            continue
            
        tokens.append(char)
        i += 1
    
    return tokens


def evaluate_expression(expression):
    operators = []
    values = []
    tokens = tokenize(expression)
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if is_number(token):
            value = float(token)
            if i > 0 and tokens[i-1] == ")":
                operators.append("*")
            values.append(value)
        
        elif token == "(":
            if i > 0 and (is_number(tokens[i-1]) or tokens[i-1] == ")"):
                operators.append("*")
            operators.append(token)
        
        elif token == ")":
            while operators and operators[-1] != "(":
                result = apply_operator(operators, values)
                if result == "undefined":
                    return None
            if operators:
                operators.pop()  # Remove '('
                if operators and operators[-1] in ["sin", "cos", "tan"]:
                    apply_operator(operators, values)
        
        elif token in ["sin", "cos", "tan"]:
            operators.append(token)
        
        elif token in precedence:
            while (operators and operators[-1] != "(" and 
                   precedence[operators[-1]] >= precedence[token]):
                result = apply_operator(operators, values)
                if result == "undefined":
                    return None
            operators.append(token)
        
        i += 1

    while operators:
        result = apply_operator(operators, values)
        if result == "undefined":
            return None

    if not values:
        return None
    
    result = values[0]
    if isinstance(result, str) and result == "undefined":
        return None
    return result

def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

# Define operator precedence
precedence = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "✕": 2,
    "➗": 2,
    "sin": 3,
    "cos": 3,
    "tan": 3,
    "√": 3,
    "^": 3,
    "(": 0,
}


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
        self.assertIsNone(tan(math.pi / 2))  # Test for undefined tangent at pi/2

    # Root Function Tests
    def test_square_root(self):
        self.assertEqual(square_root(16), 4)
        self.assertEqual(square_root(0), 0)
        self.assertIsNone(square_root(-4))  # Return None for invalid input

    def test_nth_root(self):
        self.assertEqual(nth_root(27, 3), 3)  # Cube root of 27
        self.assertEqual(nth_root(16, 4), 2)  # Fourth root of 16
        self.assertAlmostEqual(nth_root(-27, 3), -3, places=5)  # Cube root of -27
        self.assertAlmostEqual(nth_root(8, 1.5), 4, places=5)  # Non-integer root test
        self.assertAlmostEqual(nth_root(1e9, 3), 1000, places=5)  # Large exponent test
        self.assertIsNone(nth_root(-16, 2))  # Test for even root of negative number (should return None)

    def test_nth_root_complex(self):
        result = nth_root(-8, 3)
        self.assertAlmostEqual(result, -2, places=5)  # Test for negative number with odd root

class TestArithmeticAndPower(unittest.TestCase):

    # Arithmetic Function Tests
    def test_add(self):
        self.assertEqual(add(1, 1), 2)
        self.assertEqual(add(1.5, 2.5), 4.0)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)
        self.assertEqual(subtract(1.5, 0.5), 1.0)
        self.assertEqual(subtract(-5, 5), -10)
        self.assertEqual(subtract(0, 0), 0)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(2.5, 4), 10.0)
        self.assertEqual(multiply(-3, 3), -9)
        self.assertEqual(multiply(0, 10), 0)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(5.5, 2), 2.75)
        self.assertEqual(divide(-9, 3), -3)
        self.assertIsNone(divide(5, 0))  # Division by zero should return None

    # Power Function Tests
    def test_square(self):
        self.assertEqual(square(4), 16)
        self.assertEqual(square(1.5), 2.25)
        self.assertEqual(square(-3), 9)
        self.assertEqual(square(0), 0)

    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(5, 0), 1)  # Any number to the power of 0 is 1
        self.assertEqual(power(2, -1), 0.5)  # Test inverse powers
        self.assertEqual(power(-2, 3), -8)  # Negative base with odd exponent
        self.assertIsNone(power(-2, 0.5))  # Complex result should return None

if __name__ == "__main__":
    unittest.main()
