""" Program to check whether a value is palindrome."""

def check_palindrome(value):
    reversed_value = ""

    # Reversed the value using loop and string concatenation
    for char in value:
        reversed_value = char + reversed_value

    if value == reversed_value:
        print("Palindrome")
    else:
        print("Not a Palindrome")


value = input("Enter a number or string: ")
check_palindrome(value)

# Alternative way to reverse the value using slicing
# reversed_value = value[::-1] # slice from end to start with step -1
