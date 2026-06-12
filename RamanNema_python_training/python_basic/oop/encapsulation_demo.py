"""Implement encapsulation using private variables in Bank class."""

# Encapsulation is a fundamental principle of object-oriented programming that restricts direct access to some of an object's components,
# which can prevent the accidental modification of data. 
# In this example, we have a Bank class with a private variable __balance that stores the account balance. 
# The class provides methods to deposit money and display the balance, but the balance cannot be accessed or modified directly from outside the class, demonstrating encapsulation.

class Bank:

    # Private variable to store account balance (__ indicates private variable)
    # The balance variable is not directly accessible from outside the class, ensuring encapsulation.
    def __init__(self, balance):
        self.__balance = balance

    # Add amount to balance
    def deposit(self, amount):
        self.__balance += amount

    # Display current balance
    def display_balance(self):
        print("Available Balance =", self.__balance)


# Get user input
initial_balance = int(input("Enter Initial Balance: "))
deposit_amount = int(input("Enter Deposit Amount: "))

# Creating bank account object
account = Bank(initial_balance)

# Deposit amount
account.deposit(deposit_amount)

# Display updated balance
account.display_balance()

# Attempting to directly access the private variable will not work and will demonstrate encapsulation
account.__balance = 1000  # This will not change the actual balance due to private variable declaration
account.display_balance()  # The balance will still show the original balance, demonstrating encapsulation