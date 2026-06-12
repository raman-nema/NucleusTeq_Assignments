""" Program to count frequency of characters in a string using dictionary."""

# Input string
input_string = input("Enter a string: ").lower()  # convert to lowercase

# Creating an empty dictionary to store character frequencies
char_frequency = {}

# Counting frequency of each character in the input string
for char in input_string:
    if char in char_frequency:
        char_frequency[char] += 1
    else:
        char_frequency[char] = 1

# Displaying the character frequencies
print("Character Frequency in the String:")
for char, frequency in char_frequency.items():
    print(f"'{char}': {frequency}")
