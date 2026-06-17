""" Use map() to convert a list of numbers into their squares. """

if __name__ == "__main__":

    numbers = [1, 2, 3, 4, 5]

    # Using map() and lambda to calculate squares
    squares = list(map(lambda number: number ** 2, numbers))

    print(f"Before: {numbers}")
    print(f"After: {squares}")