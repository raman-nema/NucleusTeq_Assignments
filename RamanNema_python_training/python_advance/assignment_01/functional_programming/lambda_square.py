"""Find the square of a number using a lambda function."""

if __name__ == "__main__":    
    user_input = int(input("Enter the value: "))

    # Lambda function to calculate the square of a number
    square = lambda number: number ** 2 
    
    print(f"The square of {user_input} is: {square(user_input)}")