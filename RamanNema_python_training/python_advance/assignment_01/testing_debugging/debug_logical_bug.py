"""Create a function with a logical bug and use pdb to identify the issue."""

# Importing the Python debugger module.
import pdb

def calculate_sum():
    total = 0

    for number in range(1, 6):
        # Pause execution for debugging.
        pdb.set_trace()

        # Intentional bug:
        # Bug: subtraction is used instead of addition. -> found using the python debugger module
        total -= number

    print("Total:", total)


if __name__ == "__main__":
    calculate_sum()