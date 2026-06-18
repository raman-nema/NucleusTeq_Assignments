""" Write a program to create two threads that print numbers from 1 to 5 simultaneously."""

# Importing the threading module to work with threads.
import threading

def print_numbers():
    for number in range(1, 6):
        print(number)

if __name__ == "__main__":
    # Creating the first thread and assign the print_numbers function as its target.
    thread_1 = threading.Thread(target=print_numbers)
    # same for the second one
    thread_2 = threading.Thread(target=print_numbers)

    # Starting the first and second thread.
    thread_1.start()
    thread_2.start()

    # Wait for the first thread to finish execution.
    thread_1.join()

    # Wait for the second thread to finish execution.
    thread_2.join()

    # Printing a message after both threads have completed.
    print("Both threads have finished execution.")