""" Program to remove duplicates from a list using set. """

# List with duplicate numbers
number_list = [10, 20, 20, 30, 40, 40, 50]

# Removing duplicates by converting the list to a set and back to a list
unique_numbers = list(set(number_list))

print("Original List =", number_list)
print("List After Removing Duplicates =", unique_numbers)