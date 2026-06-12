""" Program to create a student dictionary and access values. """

# Creating a dictionary to store student information
student = {
    "name": "Raman",
    "age": 24,
    "course": "Python",
    "city": "Indore",
    "marks": 85.5

}

# Accessing values from the dictionary using keys
print("Name =", student["name"])
print("Age =", student["age"])
print("Course =", student["course"])
print("City =", student["city"])
print("Marks =", student["marks"])


# Displaying key-value pairs in the dictionary
print("Dictionary Items:")
print(student.items())