"""Write a generator to produce Fibonacci numbers. """

def fibonacci_generator(limit):
    first_number = 0
    second_number = 1

    for x in range(limit):
        yield first_number
        first_number, second_number = second_number, first_number + second_number # Simultaneous state update

if __name__ == "__main__":
    try:
        limit = int(input("Enter limit: "))
        if limit <= 0:
            raise ValueError("The limit must be greater than 0.")
        for num in fibonacci_generator(limit):
            print(num)
            
    except ValueError as error:
        print(f"Error: {error}")