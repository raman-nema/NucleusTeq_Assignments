""" Program to reverse a list without using reverse()."""

# Function to reverse a list without using reverse()
def reverse_list(numbers):
    reversed_list = []

    # Starting from the last index and append elements to the reversed_list
    index = len(numbers) - 1

    # Loop until the index is greater than or equal to 0
    while index >= 0:
        reversed_list.append(numbers[index]) # Append the current element to the reversed_list
        index -= 1

    print("Reversed List =", reversed_list)

number_list = []
count = int(input("How many numbers do you want to enter? "))
for i in range(count):
    number = int(input("Enter a number: "))
    number_list.append(number)

print("Original List =", number_list)
reverse_list(number_list)