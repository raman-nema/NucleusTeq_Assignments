"""Write a program using try-except-else-finally to read a number from a file  and print its square."""

def read_number_and_square() -> None:
    # Reading number from file and calculate square.
    try:
        file = open("sample_files/number.txt", "r") # Relative path to the file containing the number.
        number = int(file.read())

    # Handling FileNotFoundError if the file does not exist.
    except FileNotFoundError:
        print("File not found.")

    # Handling ValueError if the content of the file is not a valid integer.
    except ValueError:
        print("Invalid number in file.")

    # If no exceptions occurs then calculating and printing the square of the number.
    else:
        print(f"Square: {number ** 2}")

    # The finally block will always execute, regardless of whether an exception occurred or not.
    finally:
        print("Program execution completed.")


if __name__ == "__main__":
    read_number_and_square()