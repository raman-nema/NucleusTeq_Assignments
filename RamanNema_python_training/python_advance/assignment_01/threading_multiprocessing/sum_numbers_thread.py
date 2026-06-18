""" Create a thread that calculates the sum of numbers from 1 to 100. """

# Importing the threading module to work with threads.
import threading

def calculate_sum():
    total = sum(range(1, 101))
    print("Sum:", total)

if __name__ == "__main__":
    # Creating a thread and assign the calculate_sum function as its target.
    thread = threading.Thread(target=calculate_sum)

    # Starting the thread.
    thread.start()

    # Waiting for the thread to finish execution.
    thread.join()

    print("Thread execution completed.")