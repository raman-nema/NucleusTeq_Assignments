"""Create an iterator from a list and access elements using next()."""

def iterate_list() -> None:
    # Printing list elements using next().
    num = [10, 20, 30, 40, 50]

    # Converting the list into an iterator object.
    num_iterator = iter(num)

    # Using next() to retrieve the elements and advance the pointer.
    print(next(num_iterator))
    print(next(num_iterator))
    print(next(num_iterator))
    print(next(num_iterator))
    print(next(num_iterator))


if __name__ == "__main__":
    iterate_list()