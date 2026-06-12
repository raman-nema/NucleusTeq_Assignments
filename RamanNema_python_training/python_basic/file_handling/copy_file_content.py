"""Copy content from one file to another."""

# Note: copying file ie. source file will override the content of the destination file, if it already exists.

# Opening the source file in read mode
source_file = open("sample_files/source.txt", "r")

# Reading the content of the source file
content = source_file.read()

# Closing the source file
source_file.close()

# Opening the destination file in write mode
destination_file = open("sample_files/destination.txt", "w")

# Writing the content to the destination file
destination_file.write(content)

# Closing the destination file
destination_file.close()

print("File copied successfully.")