""" Use pdb breakpoints inside a loop and inspect variable values. """

# Importing the Python debugger module.
import pdb

if __name__ == "__main__":
    numbers = [10, 20, 30, 40]

    for number in numbers:
        # Pause execution at each iteration.
        pdb.set_trace()

        print(number)