""" Write a recursive function to calculate factorial."""

def factorial(number):
    # Base case
    if number == 0 or number == 1:
        return 1

    # Recursive condition
    return number * factorial(number - 1)


if __name__ == "__main__":
    user_input = int(input("Enter the number: "))
    print(f"The factorial of {user_input} is: {factorial(user_input)}")