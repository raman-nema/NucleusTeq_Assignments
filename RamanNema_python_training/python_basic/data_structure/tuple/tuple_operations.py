""" Program to create a tuple and access elements. """

# Creating a tuple with student details
student_details = ("Raman", 24, "Python", "Bhopal", 85.5)

print("Student Details Tuple:")
print(student_details)

# Accessing elements of the tuple using indexing
print("\nAccessing Elements:")
print("Name   :", student_details[0])
print("Age    :", student_details[1])
print("Course :", student_details[2])
print("City   :", student_details[3])
print("Marks  :", student_details[4])

# Displaying the length of the tuple
print("\nTuple Information:")
print("Total Elements :", len(student_details))

# Accessing the last element of the tuple using negative indexing
print("\nUsing Negative Indexing:")
print("Last Element :", student_details[-1])