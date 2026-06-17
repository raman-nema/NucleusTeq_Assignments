"""Create a password validation program using regex (minimum length, one digit, one special character)."""

import re

if __name__ == "__main__":
    password = input("Enter password: ")

    # Regular expression pattern to validate the password.
    # Requirements:
    # - At least one digit.
    # - At least one special character.
    # - Minimum length of 12 characters.
    #
    # (?=.*\d) ensures that the password contains at least one digit.
    # (?=.*[@$!%*?&]) ensures that the password contains at least one special character.
    pattern = r"^(?=.*\d)(?=.*[@$!%*?&]).{12,}$"

    # Check whether the password matches the required pattern.
    if re.match(pattern, password):
        print("Valid password")
    else:
        print("Invalid password")