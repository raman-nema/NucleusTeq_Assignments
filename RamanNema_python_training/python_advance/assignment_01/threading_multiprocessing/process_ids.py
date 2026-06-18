""" Write a program to create two processes that print their Process IDs. """

# Import the multiprocessing module to work with processes and access os functionality.
import multiprocessing
import os

# Function to print the Process ID of the current process.
def show_process_id():
    print("Process ID:", os.getpid())

if __name__ == "__main__":
    # Creating the  processes and assigning the show_process_id function as its target.
    process_1 = multiprocessing.Process(target=show_process_id)
    process_2 = multiprocessing.Process(target=show_process_id)

    # Starting the processes.
    process_1.start()
    process_2.start()

    # Wait for the first and then second process to finish execution.
    process_1.join()
    process_2.join()

    # Print a message after both processes have completed.
    print("Both processes have finished execution.")