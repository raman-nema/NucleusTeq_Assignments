"""Generate square numbers up to N."""

def generate_squares(limit):
    # Yield square numbers.
    for number in range(1, limit + 1):
        yield number ** 2

if __name__ == "__main__":
    user_lim = int(input("Enter the limit: "))
    for square in generate_squares(user_lim):
        print(square)
    