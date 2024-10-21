from calculator import evaluate_expression
import pytest

def test_expressions(filename):
    failed_lines = []

    with open(filename, 'r') as f:
        for line in f:
            print("Testing " + line.strip(), end="")

            # Split the line into left-hand side (expression) and right-hand side (expected result)
            lhs, rhs = line.strip().split('=')
            
            # Handle 'undefined' separately, otherwise convert expected result to float
            if rhs.strip() == 'undefined':
                expected = None
            else:
                try:
                    expected = float(rhs.strip())  # Try converting the expected value to float
                except ValueError:
                    print(f"Failed to convert expected result: {rhs}")
                    continue  # Skip this line if the expected value can't be parsed
                
            # Evaluate the left-hand side expression
            try:
                result = evaluate_expression(lhs.strip())
                print(f" | Got: {result}")

                # Compare result to expected value
                if expected is None:
                    assert result is None
                else:
                    assert pytest.approx(expected, abs=1e-6) == result

                print(" | Line passed")
            except Exception as e:
                print(f" | Error: {str(e)}")
                failed_lines.append((line, expected, result))
            print()

    # Report failed lines
    if failed_lines:
        print("\nFailed lines:")
        for line, expected, result in failed_lines:
            print(f"  {line.strip()} expected: {expected}, got: {result}")
    else:
        print("All test cases passed")


if __name__ == "__main__":
    test_expressions("tests.txt")
