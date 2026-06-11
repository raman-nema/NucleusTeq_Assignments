""" Program to use math module functions. """

# Importing math module to perform mathematical operations
import math

# Function to perform various math operations on the given number
def perform_math_operations(number):
    print("Square Root =", math.sqrt(number)) # Square root of the number
    print("Power =", math.pow(number, 2)) # Number raised to the power of 2
    print("Factorial =", math.factorial(number)) # Factorial of the number


user_number = int(input("Enter a number: "))
perform_math_operations(user_number)