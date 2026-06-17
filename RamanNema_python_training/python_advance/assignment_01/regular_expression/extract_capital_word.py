""" Use re.findall() to extract all words starting with a capital letter."""

# importing the regular expression module.
import re

if __name__ == "__main__":
    sentence = input("Enter the sentence: ")

    # Main logic ie. to extract all words whose first letter is uppercase.
    words = re.findall(r"\b[A-Z][a-zA-Z]*\b", sentence) 

    print(words)