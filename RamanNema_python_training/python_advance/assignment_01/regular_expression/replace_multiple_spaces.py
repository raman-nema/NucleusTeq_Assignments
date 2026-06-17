""" Replace multiple spaces in a string with a single space using re.sub(). """

import re

if __name__ == "__main__":
    sentence = input("Enter the sentence: ")

    # Replacing one or more spaces with a single space.
    updated_sentence = re.sub(r"\s+", " ", sentence) # \s+ -> " " ie. one or more space to one

    print(updated_sentence)