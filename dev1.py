class Calculator:
    
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return "Error: Cannot divide by zero."

    @staticmethod
    def square(a):
        result = a * a
        if abs(result) == float('inf'):
            return "Error: Overflow occurred."
        return result

    @staticmethod
    def power(a, n):
        try:
            result = a ** n
            if result == float('inf') or result == float('-inf'):
                return "Error: Overflow occurred."
            return result
        except OverflowError:
            return "Error: Overflow occurred."



