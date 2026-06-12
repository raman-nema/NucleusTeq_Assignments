"""Read a file and count words, lines, and characters."""

# Open the file in read mode
# Note : Here the location of the file is "sample_files/sample.txt". We can change it to the location of our file.
file = open("sample_files/sample.txt", "r")

# Read the entire content of the file
content = file.read()

# Close the file after reading
file.close()

# Counting lines, words, and characters
lines = len(content.split("\n"))
words = len(content.split())
characters = len(content)

# Printing the results
print("Lines:", lines)
print("Words:", words)
print("Characters:", characters)