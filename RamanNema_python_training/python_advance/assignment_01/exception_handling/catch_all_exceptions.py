""" Catch all exceptions while accessing a list element. """

def access_list_element() -> None:
    numbers = [10, 20, 30]
    try:
        index = int(input("Enter index: "))
        print("Element:", numbers[index])

    except ValueError:
        print("Error: Please enter a valid integer, not text.")
        
    except IndexError:
        print(f"Error: Index out of range. Please enter a number between -3 and 2.")
        
    except Exception as error:
        # This is the safety net for literally anything else
        print(f"An unexpected error occurred: {error}")

if __name__ == "__main__":
    access_list_element()