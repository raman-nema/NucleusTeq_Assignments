""" Create a module with two utility functions and import it into another Python file."""

# importing the functions from another module.
from utility_functions import greet, square, cube

if __name__ == "__main__":
    greet("Raman")
    square(5)
    cube(5)