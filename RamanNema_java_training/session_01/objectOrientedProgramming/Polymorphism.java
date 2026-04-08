/*
2. Demonstrate polymorphism by creating methods with the same name but different parameters in a parent and child class.

Polymorphism in Java
Polymorphism means "many forms".
It allows a method to perform different tasks based on the object or parameters.

Types of Polymorphism:
a. Compile-time Polymorphism (Method Overloading)
   - Same method name with different parameters
   - Decided at compile time

b. Runtime Polymorphism (Method Overriding)
   - Child class provides its own implementation of a parent class method
   - Decided at runtime using dynamic method dispatch

Advantages:
- Improves code flexibility and reusability
- Allows one interface to be used for different implementations
*/

// Example: Student02 and GraduateStudent02 classes demonstrating polymorphism

package RamanNema_java_training.session_01.objectOrientedProgramming;
// Parent class
class Student02 {
    // Method
    public void show() {
        System.out.println("I am a Student");
    }

    // Method Overloading
    public void show(String name) {
        System.out.println("Student Name: " + name);
    }
}

// Child class
class GraduateStudent02 extends Student02 {

    // Method Overriding
    @Override
    public void show() {
        System.out.println("I am a Graduate Student");
    }
}

// Main class
public class Polymorphism {
    public static void main(String[] args) {

        Student02 s = new Student02();
        s.show();                 // Parent method
        s.show("Shubham");        // Overloaded method

        GraduateStudent02 g = new GraduateStudent02();
        g.show();                 // Overridden method
    }
}