""" Program to reverse a number using loop. """

def reverse_number(number):
    reversed_number = 0

    # Reverse each digit
    while number > 0:
        digit = number % 10 # get the last digit

        # shift the previous digits to left and add the new digit
        reversed_number = reversed_number * 10 + digit 

        # remove the last digit from the original number
        number = number // 10

    print("Reversed Number =", reversed_number)


user_number = int(input("Enter a number: "))
reverse_number(user_number)