""" Write a program to extract all numbers from a given string using regular expressions."""

# Imported the regular expression module re
import re

if __name__ == "__main__":
    text = "I have 10 books and 12 pens along with 5 set of erasers."

    # Using the regular expression pattern '\d+' to find all numbers in the string.
    numbers = re.findall(r"\d+", text)

    print(numbers)