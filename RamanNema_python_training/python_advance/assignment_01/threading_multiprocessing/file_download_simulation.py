""" Create multiple threads to simulate file downloading using time.sleep(). """

# Import the threading and time modules.
import threading
import time

# Function to simulate downloading a file.
def download_file(file):
    print(f"Downloading {file}...")

    # Pause execution for 2 seconds to simulate download time.
    time.sleep(2)

    print(f"{file} downloaded.")

if __name__ == "__main__":
    # Create threads for downloading different files.
    thread_1 = threading.Thread(target=download_file, args=("File1.pdf",))
    thread_2 = threading.Thread(target=download_file, args=("File2.pdf",))
    thread_3 = threading.Thread(target=download_file, args=("File3.pdf",))

    # Start all threads.
    thread_1.start()
    thread_2.start()
    thread_3.start()

    # Wait for all threads to finish execution.
    thread_1.join()
    thread_2.join()
    thread_3.join()

    # Print a message after all downloads are complete.
    print("All files downloaded successfully.")