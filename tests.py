from calculator import evaluate_expression
import pytest

def test_expressions(filename):
    anyFail = False

    with open(filename, 'r') as f:
        for line in f:
            print("Testing " + line, end="")
            lhs, rhs = line.strip().split('=')
            if rhs == 'undefined':
                expected = None
            else:
                expected = float(rhs)
            try:
                result = evaluate_expression(lhs)
                print("Got " + str(result))
                if expected is None:
                    assert result is None
                else:
                    assert pytest.approx(expected) == result
                print("Line passed")
            except Exception as e:
                print(str(e))
                print("Line failed")
                anyFail = True
            print()

    if anyFail:
        print("Some tests failed")
    else:
        print("All test cases passed")

if __name__ == "__main__":
    test_expressions("tests.txt")