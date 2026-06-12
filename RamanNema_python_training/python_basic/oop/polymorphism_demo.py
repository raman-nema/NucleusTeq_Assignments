""" Demonstrate polymorphism using different classes with the same method name. """

# Polymorphism allows objects of different classes to be treated as objects of a common superclass. 
# In this example, we have different employee roles (Developer, Tester, Designer, Project Manager) that all have a method named 'work'.
# Each class implements the 'work' method differently, demonstrating polymorphism.

class Developer:
    # Method to describe developer's work
    def work(self):
        print("Developer writes and maintains code.")


class Tester:
    # Method to describe tester's work
    def work(self):
        print("Tester verifies application functionality.")


class Designer:
    # Method to describe designer's work
    def work(self):
        print("Designer creates user interface designs.")


class ProjectManager:
    # Method to describe project manager's work
    def work(self):
        print("Project Manager plans and manages project activities.")

# Create instances of each employee role
developer = Developer()
tester = Tester()
designer = Designer()
project_manager = ProjectManager()

# Create a list of employees and call the work method for each employee to demonstrate polymorphism
employees = [developer, tester, designer, project_manager]

# Loop through the list of employees and call the work method for each employee
for employee in employees:
    employee.work()