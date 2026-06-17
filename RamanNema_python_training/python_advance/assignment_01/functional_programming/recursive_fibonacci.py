""" Write a recursive function to calculate Fibonacci. """

def fibonacci(number):
    # Base Case
    if number <= 1:
        return number

    # Recursive Condition
    return fibonacci(number - 1) + fibonacci(number - 2)

if __name__ == "__main__":
    size = int(input("Enter the limit: "))
    for number in range(size):
        print(fibonacci(number))