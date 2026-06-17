""" Write a regular expression to validate an email address. """

import re

if __name__ == "__main__":
    email = input("Enter email: ")
    
    # pattern for matching the email
    pattern = r"^[A-Za-z0-9]+([._%+-][A-Za-z0-9]+)*@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$"

    if re.match(pattern, email):
        print("Valid email")
    else:
        print("Invalid email")