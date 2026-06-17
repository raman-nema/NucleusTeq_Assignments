""" Write a regular expression to validate a 10-digit mobile number. """

import re

if __name__ == "__main__":
    mobile_no = input("Enter the mobile number: ")

    # main logic for the validation
    pattern = r"^\d{10}$"

    # re.match() matches our input with pattern
    if re.match(pattern, mobile_no):
        print("Valid number.")
    else:
        print("Invalid number")