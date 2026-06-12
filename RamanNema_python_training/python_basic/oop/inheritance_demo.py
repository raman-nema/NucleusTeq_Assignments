""" Implement inheritance using Person and Employee classes. """

# The Person class has attributes like name, age, and city, and methods to display information and greet.
class Person:
    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city

    def display_info(self):
        print("Name:", self.name)
        print("Age:", self.age)
        print("City:", self.city)

    def greet(self):
        print(f"Hello, my name is {self.name}.")

# The Employee class inherits from the Person class and adds additional attributes like employee_id and department, along with a method to display employee-specific information.
class Employee(Person):
    def __init__(self, name, age, city, employee_id, department):
         # super is used to call the constructor of the parent class (Person) to initialize the inherited attributes.
        super().__init__(name, age, city)
        self.employee_id = employee_id
        self.department = department

    def display_employee_info(self):
        print("Employee ID:", self.employee_id)
        print("Department :", self.department)


# Creating an Employee object
employee = Employee("Raman Nema", 22, "Indore", "E123", "IT")

# Accessing methods
employee.display_info()
employee.display_employee_info()
employee.greet()