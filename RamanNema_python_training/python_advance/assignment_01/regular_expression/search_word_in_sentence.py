""" Use re.search() to check whether a word exists in a sentence."""

import re

if __name__ == "__main__":
    sentence = input("Enter the sentence: ")
    word = input("Enter word to search: ")

    # re.search is used for searching
    if re.search(word, sentence):
        print("Word found")
    else:
        print("Word not found")