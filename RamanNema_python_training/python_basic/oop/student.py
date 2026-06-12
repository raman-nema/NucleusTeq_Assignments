""" Program to create a Student class."""

# The Student class has attributes like student_id, name, age, and course.
class Student:

    # The __init__ method initializes the attributes of the Student class.
    def __init__(self, student_id, name, roll_no, age, course):
        self.student_id = student_id
        self.name = name
        self.roll_no = roll_no
        self.age = age
        self.course = course

    # The display_details method prints the details of the student.
    def display_details(self):
        print("Student ID:", self.student_id)
        print("Name:", self.name)
        print("Roll No:", self.roll_no)
        print("Age:", self.age)
        print("Course:", self.course)

# Creating an instance of the Student class and display its details.
student = Student(101, "Raman Nema", 4, 22, "Python")

# Calling the display_details method to print the student's information.
student.display_details()