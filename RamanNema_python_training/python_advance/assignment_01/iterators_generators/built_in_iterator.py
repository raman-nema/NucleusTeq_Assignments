"""Show an example of a built-in generator (like range) and iterate over it."""

def iterate_range() -> None:
    # Iterating over range using iter and next.
    range_iterator = iter(range(1, 6))

    print(next(range_iterator))
    print(next(range_iterator))
    print(next(range_iterator))
    print(next(range_iterator))
    print(next(range_iterator))


if __name__ == "__main__":
    iterate_range()