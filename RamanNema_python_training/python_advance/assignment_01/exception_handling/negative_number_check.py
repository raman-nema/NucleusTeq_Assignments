""" Create a function that raises a ValueError if a number is negative. """

def negative_number_check(number: int) -> None:
    # Check whether the provided number is negative.
    if number < 0:
        raise ValueError("Negative numbers are not allowed.")

    print("Valid number.")


if __name__ == "__main__":
    try:
        user_number = int(input("Enter a number: "))
        # Validating the entered number.
        negative_number_check(user_number)

    except ValueError as error:
        print(error)