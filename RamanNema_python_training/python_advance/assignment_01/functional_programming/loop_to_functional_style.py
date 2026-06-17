"""Convert a simple loop-based program into a functional style using filter()."""

if __name__ == "__main__":
    marks = [35, 80, 45, 90, 25, 60]

    # Loop-based approach
    passed_students = []

    for mark in marks:
        if mark >= 40:
            passed_students.append(mark)

    print("Loop-based output:", passed_students)

    # Functional approach using filter() 
    passed_students = list(filter(lambda mark: mark >= 40, marks))

    print("Functional output:", passed_students)