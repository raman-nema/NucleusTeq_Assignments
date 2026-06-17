""" Write a pattern to check if a string contains only alphabets. """

import re

if __name__ == "__main__":
    text = input("Enter text: ")

    pattern = r"^[A-Za-z]+$" # spaces are not alphabets

    if re.match(pattern, text):
        print("Contains only alphabets")
    else:
        print("Contains other characters")  