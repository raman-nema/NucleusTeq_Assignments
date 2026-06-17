""" Write a program to divide two numbers entered by the user and handle ZeroDivisionError. """

def divide_numbers() -> None:
    # Perform division safely.
    try:
        num1 = float(input("Enter numerator: "))
        num2 = float(input("Enter denominator: "))

        result = num1 / num2
        print(f"Result: {result}")

    # Handling ZeroDivisionError if the user tries to divide by zero.
    except ZeroDivisionError:
        print("Cannot divide by zero.")

    # Handling ValueError if the user enters invalid numbers.
    except ValueError:
        print("Please enter valid input.")

if __name__ == "__main__":
    divide_numbers()