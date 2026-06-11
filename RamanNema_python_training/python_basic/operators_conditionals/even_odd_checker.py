# Program to check whether a number is even or odd.

def check_even_or_odd(number):
    # Check divisibility by 2
    if number % 2 == 0:
        print("The number is Even.")
    else:
        print("The number is Odd.")


user_number = int(input("Enter a number: "))
check_even_or_odd(user_number)