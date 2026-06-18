""" Demonstrate the use of join() in threading."""

# Import the threading and time modules.
import threading
import time

def perform_task():
    print("Thread started.")
    # Pause execution for 3 seconds.
    time.sleep(3)
    print("Thread finished.")

if __name__ == "__main__":
    # Creating a thread and assign the perform_task function as its target.
    thread = threading.Thread(target=perform_task)

    # Start the thread.
    thread.start()

    # Wait for the thread to complete before moving to the next statement.
    thread.join()

    # This line executes only after the thread has finished.
    print("Main program finished.")