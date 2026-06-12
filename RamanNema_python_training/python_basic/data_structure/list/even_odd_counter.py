""" Program to count even and odd numbers in a list."""

# Function to count even and odd numbers in a list
def count_even_odd(numbers):
    even_count = 0
    odd_count = 0

# Iterate through the list and count even and odd numbers
    for number in numbers:
        if number % 2 == 0:
            even_count += 1
        else:
            odd_count += 1

    print("Even Numbers =", even_count)
    print("Odd Numbers =", odd_count)

# Main program
number_list = []
count = int(input("How many numbers do you want to enter? "))
# Loop to get the numbers from the user and append them to the list
for i in range(count):
    number = int(input("Enter a number: "))
    number_list.append(number)

count_even_odd(number_list)