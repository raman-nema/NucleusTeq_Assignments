# Program to swap two numbers.

def swap_numbers(first_number, second_number):
    # Swap two numbers and return them.
    first_number, second_number = second_number, first_number
    return first_number, second_number

number1 = int(input("Enter first number: "))
number2 = int(input("Enter second number: "))

number1, number2 = swap_numbers(number1, number2)

print("Numbers after swapping:")
print("First Number =", number1)
print("Second Number =", number2)