# Program to perform basic arithmetic operations.

def calculate_operations(first_number, second_number):
    # Display arithmetic operations.

    print("Sum =", first_number + second_number)
    print("Difference =", first_number - second_number)
    print("Multiplication =", first_number * second_number)

    if second_number != 0:
        print("Division =", first_number / second_number)
    else:
        print("Division cannot be performed because denominator is zero.")


number1 = float(input("Enter first number: "))
number2 = float(input("Enter second number: "))

calculate_operations(number1, number2)