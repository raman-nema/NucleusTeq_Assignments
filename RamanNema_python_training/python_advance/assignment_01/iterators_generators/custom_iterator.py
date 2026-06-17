"""Return numbers from 1 to N using a custom iterator."""

class NumberIterator:
    def __init__(self, max):
        # Storing the maximum number.
        self.max = max

        # Starting counting from 1.
        self.num = 1

    def __iter__(self):
        # Returning the iterator object itself.
        return self

    def __next__(self):
        # Checking if the current number is within the limit.
        if self.num <= self.max:
            result = self.num
            self.num += 1
            return result

        # Stopping iteration when the limit is reached.
        raise StopIteration

if __name__ == "__main__":
    limit = int(input("Enter the limit: "))

    # Create an iterator that returns numbers from 1 to 5.
    iterator = NumberIterator(limit)

    # Print each number returned by the iterator.
    for number in iterator:
        print(number)