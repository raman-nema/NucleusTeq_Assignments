""" Write pytest test cases for a function that adds two numbers. """

def add_numbers(first_number, second_number):
    return first_number + second_number


def test_add_positive_numbers():
    assert add_numbers(2, 3) == 5


def test_add_negative_numbers():
    assert add_numbers(-2, -3) == -5


def test_add_zero():
    assert add_numbers(5, 0) == 5

def test_random():
    assert add_numbers(10000,10000) == 20000

# All test cases passed.