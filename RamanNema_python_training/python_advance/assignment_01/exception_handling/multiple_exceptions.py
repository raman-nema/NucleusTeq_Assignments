""" Handle multiple exceptions  in a single program. """

def handle_multiple_exceptions() -> None:
    try:
        number = int(input("Enter a number: "))
        result = 100 / number

        file = open("sample_files/number.txt", "r") # Relative path to the file containing the number.
        print(file.read())

        print(result)

    # ValueError can occur if the user enters a non-integer value.
    except ValueError:
        print("Invalid integer entered.")
    
    # ZeroDivisionError can occur if the user enters zero as the number.
    except ZeroDivisionError:
        print("Division by zero is not allowed.")
    
    # FileNotFound occur if the file does not exist
    except FileNotFoundError:
        print("File does not exist.")


if __name__ == "__main__":
    handle_multiple_exceptions()