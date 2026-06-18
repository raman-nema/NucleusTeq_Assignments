"""Create a package with two modules and include an __init__.py file."""

# importing various functions of modules from the student_package
from student_package.student_info import get_student_details
from student_package.student_marks import get_student_marks, calculate_average


if __name__ == "__main__":
    student = get_student_details()
    marks = get_student_marks()

    print("\nStudent Details- ")
    print("Name:", student["name"])
    print("Roll Number:", student["roll_number"])
    print("Course:", student["course"])

    print("\nMarks- ")
    for subject, mark in marks.items():
        print(f"{subject}: {mark}")

    print("\nAverage Marks:", calculate_average(marks))