""" Write a program that takes a number as input and handles ValueError if the input is not a valid integer. """

def get_int_input() -> None:
    # Taking integer input from user and handle ValueError.
    try:
        number = int(input("Enter an integer: "))
        print(f"You entered: {number}")
    # Handles ValueError if the input is not a valid integer.
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

# Calling the function to get integer input from user.
if __name__ == "__main__":
    get_int_input()