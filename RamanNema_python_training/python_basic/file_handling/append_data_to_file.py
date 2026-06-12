"""Append data to an existing file."""

# Opening the file in append mode using 'a'. If the file does not exist, it will be created.
file = open("sample_files/notes.txt", "a")

# Appending new data to the file. The "\n" ensures that the new data is added on a new line.
file.write("\nAppended text in notes file from Python.")

# Closing the file to save the changes.
file.close()

print("Data appended successfully.")