"""Student marks module."""

def get_student_marks():
    return {
        "Python": 85,
        "Java": 90,
        "Database": 88
    }


def calculate_average(marks):
    return sum(marks.values()) / len(marks)