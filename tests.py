from calculator import evaluate_expression
import pytest

def test_expressions(filename):
    with open(filename, 'r') as f:
        for line in f:
            print("Testing " + line, end="")
            lhs, rhs = line.strip().split('=')
            expected = float(rhs)
            result = evaluate_expression(lhs)
            assert pytest.approx(expected) == result
            print("Line passed")

    print("All test cases passed")

if __name__ == "__main__":
    test_expressions("tests.txt")