""" Program to find the maximum number from a list. """

def find_maximum_number(numbers):
    maximum_number = numbers[0]

    for i in range(len(numbers)):
        if numbers[i] > maximum_number:
            maximum_number = numbers[i]
    return maximum_number

list = [12, 45, 67, 23, 89, 34]
print("Maximum Number =", find_maximum_number(list))

# Alternative way to find the maximum number using built-in max() function
# print("Maximum Number =", max(list));
