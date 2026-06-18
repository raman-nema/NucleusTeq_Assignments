"""Use calculator package."""

# importing various functions from calculator package
from calculator_package.add import add
from calculator_package.subtract import subtract
from calculator_package.multiply import multiply
from calculator_package.divide import divide

if __name__ == "__main__":
    print("Addition:", add(10, 5))
    print("Subtraction:", subtract(10, 5))
    print("Multiplication:", multiply(10, 5))
    print("Division:", divide(10, 5))