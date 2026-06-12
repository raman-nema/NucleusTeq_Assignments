"""Search a word in a file."""

# Get the word to search from the user
word = input("Enter a word to search: ")

# Opening the file in read mode
file = open("sample_files/sample.txt", "r")

# Reading the content of the file
content = file.read()

# Closing the file
file.close()

# Checking if the word is in the content
if word in content:
    print("Word found!.")
else:
    print("Word not found!.")