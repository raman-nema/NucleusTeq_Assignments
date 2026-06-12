""" Program to convert tuple into list and modify it. """

# Creating a tuple with numbers
numbers_tuple = (10, 20, 30, 40)

# Converting the tuple to a list
numbers_list = list(numbers_tuple)

# Displaying the original tuple and the converted list
print("Original Tuple =", numbers_tuple)
print("Converted List =", numbers_list)
numbers_list.append(50)

# Displaying the modified list after adding a new element
print("Modified List =", numbers_list)

# Displaying the original tuple to show that it remains unchanged
print("Original Tuple after modification =", numbers_tuple)