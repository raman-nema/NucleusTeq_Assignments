""" Create a custom exception called AgeException and raise it if age is less than 18. """

class AgeException(Exception):
    # Initialized the custom exception with the entered age.
    def __init__(self, age):
        self.age = age
        super().__init__(
            f"Access denied: Age {age} is below the minimum required age of 18."
        )


def verify_age(age):
    # Checking if the entered age is less than 18.
    if age < 18:
        # Raise the custom exception.
        raise AgeException(age)
    
    # Returning a success message for  valid age.
    return f"Access granted! Age {age} is valid."

if __name__ == "__main__":
    age = int(input("Enter your age: "))
    try:
        result = verify_age(age)
        print(result)
    except AgeException as error:
        # Displaying the custom exception message.
        print(f"AgeException caught: {error}")