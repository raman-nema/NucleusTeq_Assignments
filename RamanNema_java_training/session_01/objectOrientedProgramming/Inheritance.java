/*
Object Oriented Programming (OOP):
1. Implement inheritance to create a "GraduateStudent" class that extends the "Student" class with additional features.

Inheritance in Java:
Inheritance is an OOP concept where one class (child/subclass)
acquires the properties and behaviors of another class (parent/superclass).

Key Points:
a. It promotes code reusability.
b. It is achieved using the 'extends' keyword.
c. The child class can access public and protected members of the parent class.
d. Constructors of the parent class are called using 'super'.

Advantages:
- Reduces code duplication
- Improves maintainability
- Supports hierarchical classification
*/

// Example: Student and GraduateStudent classes demonstrating inheritance
package RamanNema_java_training.session_01.objectOrientedProgramming;

// Parent class
class Student {
    String name;
    int rollNumber;
    double marks;

    public Student(String name, int rollNumber, double marks) {
        this.name = name;
        this.rollNumber = rollNumber;
        this.marks = marks;
    }

    public void displayDetails() {
        System.out.println(name + " " + rollNumber + " " + marks);
    }
}

// Child class
class GraduateStudent extends Student {
    String specialization;

    public GraduateStudent(String name, int rollNumber, double marks, String specialization) {
        super(name, rollNumber, marks);
        this.specialization = specialization;
    }

    public void displayGraduateDetails() {
        displayDetails();
        System.out.println("Specialization: " + specialization);
    }
}

// Main class
public class Inheritance {
    public static void main(String[] args) {
        GraduateStudent g = new GraduateStudent("Raman", 102, 90, "Computer Science");
        g.displayGraduateDetails();
    }
}