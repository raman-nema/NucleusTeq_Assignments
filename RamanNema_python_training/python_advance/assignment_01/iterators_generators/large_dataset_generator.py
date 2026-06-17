""" Write a program that processes a large dataset using a generator instead of storing all values in a list."""


def generate_numbers(limit: int):
    # Generating numbers one at a time.
    for number in range(limit):
        yield number


def process_large_dataset() -> None:
    # Processing generated data.
    total = 0

    # Streaming numbers sequentially without loading a massive list into RAM with the help of generator
    for number in generate_numbers(1000000): 
        total += number

    print(f"Total: {total}")


if __name__ == "__main__":
    process_large_dataset()