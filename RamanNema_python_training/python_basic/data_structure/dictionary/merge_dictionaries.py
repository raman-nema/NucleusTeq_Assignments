""" Program to merge two dictionaries. """

# First dictionary with student information
student = {
    "student_id": 101,
    "name": "Raman",
    "age": 24,
    "city": "Indore"
}

# Second dictionary with course information
course = {
    "course_name": "Python",
    "duration": "3 Months",
    "trainer": "Naman",
    "fees": 5000
}

# Merging the two dictionaries using the update() method
merged_dict = {}

# Add data from student
merged_dict.update(student)

# Add data from course
merged_dict.update(course)

# Displaying the merged dictionary
print("Merged Dictionary:")
print(merged_dict)

# # Alternative way to merge dictionaries using dictionary unpacking
# merged_dict = {}

# # Add first dictionary
# for key in student:
#     merged_dict[key] = student[key]

# # Add second dictionary
# for key in course:
#     merged_dict[key] = course[key]

# print("Merged Dictionary =", merged_dict)