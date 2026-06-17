""" - Write pytest test cases for a function that checks whether a number is prime. """

# core logic for checking whether no is prime or not
def is_prime(number):
    if number <= 1:
        return False

    # have more than 1 factors -> not a prime no
    for value in range(2, number):
        if number % value == 0:
            return False

    # is prime no
    return True


def test_prime_number():
    assert is_prime(7) is True


def test_non_prime_number():
    assert is_prime(8) is False


def test_one():
    assert is_prime(1) is False

def test_zero():
    assert is_prime(0) is False

# All test cases passed.