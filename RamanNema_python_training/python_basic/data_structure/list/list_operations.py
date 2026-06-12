""" Program to perform operations on a list."""

def perform_list_operations(numbers):
    # Display the original list
    print("Original List:", numbers)

    # Calculate and display the sum, maximum and minimum number in the list
    print("Sum =", sum(numbers))
    print("Maximum Number =", max(numbers))
    print("Minimum Number =", min(numbers))

    # Display the sorted list
    sorted_numbers = sorted(numbers)
    print("Sorted List =", sorted_numbers)

    # Display the list after removing duplicates
    unique_numbers = list(set(numbers))
    print("List After Removing Duplicates =", unique_numbers)

# Main program
number_list = []
count = int(input("How many numbers do you want to enter? "))
# Loop to get the numbers from the user and append them to the list
for i in range(count):
    number = int(input("Enter a number: "))
    number_list.append(number)

perform_list_operations(number_list)