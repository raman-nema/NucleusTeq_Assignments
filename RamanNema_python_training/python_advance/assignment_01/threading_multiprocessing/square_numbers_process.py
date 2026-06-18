""" Write a multiprocessing program to calculate the square of numbers using Process class. """

# Importing the multiprocessing module to work with processes.
import multiprocessing

def calculate_square(number):
    print(f"Square of {number}: {number ** 2}")

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    processes = []

    for number in numbers:
        # Create a process and pass the current number as an argument.
        process = multiprocessing.Process(
            target=calculate_square,
            args=(number,)
        )
        # Add the process to the list.
        processes.append(process)
        process.start()

    # Wait for all processes to finish execution.
    for process in processes:
        process.join()

    # Print a message after all processes have completed.
    print("All processes have finished execution.")