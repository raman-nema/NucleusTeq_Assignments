# Program to calculate grade based on marks.

def calculate_grade(marks):
    # Determine grade based on marks
    if marks >= 90:
        print("Grade: A")
    elif marks >= 75:
        print("Grade: B")
    elif marks >= 50:
        print("Grade: C")
    elif marks >= 38:
        print("Grade: D")
    else:
        print("Fail")


student_marks = float(input("Enter marks: "))
calculate_grade(student_marks)