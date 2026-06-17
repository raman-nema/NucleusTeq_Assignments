""" Write a program that handles FileNotFoundError when trying to open a file. """

def open_file() -> None:
    try:
        # Opening the file in read mode.
        file = open("sample_files/data.txt", "r")
        # Displaying the file content.
        print(file.read())

    except FileNotFoundError:
        # Print a message if the file does not exist.
        print("The specified file was not found.")


if __name__ == "__main__":
    open_file()