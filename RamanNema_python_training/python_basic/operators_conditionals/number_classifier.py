# Program to check whether a number is positive, negative, or zero.

def classify_number(number):
    # Check the value of the number
    if number > 0:
        print("The number is Positive.")
    elif number < 0:
        print("The number is Negative.")
    else:
        print("The number is Zero.")


user_number = float(input("Enter a number: "))
classify_number(user_number)