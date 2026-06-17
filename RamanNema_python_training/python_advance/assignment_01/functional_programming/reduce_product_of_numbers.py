""" Use reduce() to find the product of all elements in a list. """

from functools import reduce

if __name__ == "__main__":

    numbers = [1, 2, 3, 4, 5]

    # Use reduce() to multiply all elements
    product = reduce(lambda x, y: x * y, numbers)

    print(product)