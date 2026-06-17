""" Use filter() to extract even numbers from a list. """

if __name__ == "__main__":

    numbers = [1, 2, 3, 4, 5, 6]

    # Using filter() and lambda to get even numbers
    even_numbers = list(filter(lambda number: number % 2 == 0, numbers))

    print(f"Original: {numbers}")
    # Printing the even numbers
    print(f"EvenList: {even_numbers}")