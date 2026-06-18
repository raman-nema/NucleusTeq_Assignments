"""Convert a normal function into parallel execution using ProcessPoolExecutor.

The main benefit of ProcessPoolExecutor is that it manages processes for you automatically.
Without ProcessPoolExecutor, we have to create, start, and join each process manually.

"""

# Importing ProcessPoolExecutor to manage a pool of processes.
from concurrent.futures import ProcessPoolExecutor

def square(number):
    return number ** 2

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    # Creating a process pool and automatically clean it up when done.
    with ProcessPoolExecutor() as executor:

        # Executing the square function for each number in parallel using processes.
        results = executor.map(square, numbers)

    print(list(results))