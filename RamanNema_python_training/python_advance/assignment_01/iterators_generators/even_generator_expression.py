"""Generate even numbers using generator expression."""

def display_even_numbers() -> None:
    # Generator expression to evaluate even numbers lazily
    even_numbers = (num for num in range(1, 51) if num % 2 == 0)

    # Iterating and print each generated number
    for number in even_numbers:
        print(number)


if __name__ == "__main__":
    # Execute the function
    display_even_numbers()