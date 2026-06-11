""" Program to find factorial of a number. """

def factorial(number):
    factorial = 1

    # Multiplying numbers from 1 to given number
    for count in range(1, number + 1): # since the upper limit is exclusive, so number + 1
        factorial = factorial * count
    print("Factorial =", factorial)

user_number = int(input("Enter a number: "))
factorial(user_number)