""" Program to create a Car class with constructor. """

# The Car class has attributes like brand, model, and price.
class Car:

    # The __init__ method (constructor) initializes the attributes of the Car class.
    def __init__(self, brand, model, price, date_of_manufacture):
        self.brand = brand
        self.model = model
        self.price = price
        self.date_of_manufacture = date_of_manufacture

    # The display_details method prints the details of the car.
    def display_details(self):
        print("Brand:", self.brand)
        print("Model:", self.model)
        print("Price:", self.price)
        print("Date of Manufacture:", self.date_of_manufacture, "\n")

# Creating an instance of the Car class and display its details.
car1 = Car("Hyundai", "Creta", 1500000, "2022-01-01")
car2 = Car("Maruti Suzuki", "Swift", 800000, "2021-06-15")

# Calling the display_details method to print the car's information.
car1.display_details()
car2.display_details()