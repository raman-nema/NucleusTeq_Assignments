"""Create a file and write your name into it."""

# Opening a file in write mode.
# If the file does not exist, it will be created.
# If it already exists, it will be overwritten.

# Note: The file "name.txt" will be created inside the "sample_files" folder located in the same directory as this script.

file = open("sample_files/name.txt", "w")

# Writing the name in the file.
file.write("Raman Nema")

# Closing the file to save the changes.
file.close()

print("Name written successfully.")