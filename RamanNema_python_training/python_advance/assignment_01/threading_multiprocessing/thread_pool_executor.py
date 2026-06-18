"""Convert a normal function into parallel execution using ThreadPoolExecutor.

 The main benefit of ThreadPoolExecutor is that it manages threads for you automatically.
 Without ThreadPoolExecutor, we have to create, start, and join each thread manually.

"""

# Importing ThreadPoolExecutor to manage a pool of threads.
from concurrent.futures import ThreadPoolExecutor

def square(number):
    return number ** 2

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    # Creating a thread pool and automatically clean it up when done.
    with ThreadPoolExecutor() as executor:

        # Executing the square function for each number in parallel.
        results = executor.map(square, numbers)

    print(list(results))