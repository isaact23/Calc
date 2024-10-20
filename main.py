from calculator import evaluate_expression
import sys

def main():
    if len(sys.argv) > 1:
        exp = sys.argv[1]
    else:
        print("Enter your equation: ")
        exp = input()
    res = evaluate_expression(exp)
    print("The result is " + str(res))

if __name__ == "__main__":
    main()
