import math
import re
import cmath

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

# Example usage:
expression1 = "((3.5 + 4.9) - (10 ➗ 2)) ✕ 3.40"
result1 = evaluate_expression(expression1)
print(result1)  # Should output 11.56

expression2 = "5 ➗ 0"
result2 = evaluate_expression(expression2)
print(result2)  # Should output 'undefined'

expression3 = "3√(27)"
result3 = evaluate_expression(expression3)
print(result3)  # Should output 3 (cube root of 27)

expression4 = "9999^9"
result4 = evaluate_expression(expression4)
print(result4)  # Should output a large number

expression5 = "2√(25)"
result5 = evaluate_expression(expression5)
print(result5)  # Should output 5 (square root of 25)

expression6 = "4√(625)"
result6 = evaluate_expression(expression6)
print(result6)  # Should output 5 (fourth root of 625)