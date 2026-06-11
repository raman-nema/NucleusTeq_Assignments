# Program to find the largest of three numbers.

def find_largest(first_number, second_number, third_number):
    # Compare all three numbers
    if first_number >= second_number and first_number >= third_number:
        largest_number = first_number
    elif second_number >= first_number and second_number >= third_number:
        largest_number = second_number
    else:
        largest_number = third_number

    print("Largest number is:", largest_number)


number1 = float(input("Enter first number: "))
number2 = float(input("Enter second number: "))
number3 = float(input("Enter third number: "))

find_largest(number1, number2, number3)