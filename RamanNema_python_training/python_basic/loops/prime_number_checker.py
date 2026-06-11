""" Program to check whether a number is prime. """

def check_prime_number(number):
    # negative numbers, 0 and 1 are not prime numbers
    if number <= 1:
        print("Not a Prime Number")
        return

    # check for factors from 2 to number-1
    for div in range(2, number):
        if number % div == 0:
            print("Not a Prime Number")
            return

    print("Prime Number")

user_number = int(input("Enter a number: "))
check_prime_number(user_number)