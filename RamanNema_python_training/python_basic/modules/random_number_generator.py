""" Program to generate random numbers. """

# Importing random module to generate random numbers
import random

# Function to generate and print random numbers between 1 and 10
def generate_random_numbers():
    # Generating and printing three random numbers between 1 and 10
    print("Random Number_1 =", random.randint(1, 10))  
    print("Random Number_2 =", random.randint(1, 10))
    print("Random Number_3 =", random.randint(1, 10))


generate_random_numbers()