""" Program to print multiplication table of a number."""

def print_table(number):
    # Printing table from 1 to 10
    for count in range(1, 11):
        print(f"{number} x {count} = {number * count}")
        
user_number = int(input("Enter a number: "))
print_table(user_number)