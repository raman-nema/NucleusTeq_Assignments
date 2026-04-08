/*
Advanced Topics:
 1. Explain the concept of interfaces and abstract classes with examples.

Abstract Class:
- Declared using "abstract" keyword
- Can have both abstract (no body) and non-abstract methods
- Can have constructors and instance variables
- Cannot be instantiated (no object creation)
- Used when classes are related and share common behavior

-----------------------------------------------------
Interface:
- A blueprint of a class
- Contains abstract methods by default
- Variables are public, static, and final
- Achieves multiple inheritance using "implements"
- Used to define a contract (what a class should do)

-----------------------------------------------------
Difference:
- Abstract class → partial abstraction (methods + implementation)
- Interface → full abstraction (only method definitions)

- Abstract class → extends (single inheritance)
- Interface → implements (multiple inheritance allowed)

-----------------------------------------------------

Examples of Abstract Class and Interface are menttioned below:
*/

package RamanNema_java_training.session_01.advancedTopics;
// Abstract class
abstract class Animal {
    abstract void sound(); // abstract method

    void sleep() { // normal method
        System.out.println("Animal sleeps");
    }
}

// Interface
interface Pet {
    void play(); // abstract method
}

// Child class
class Dog extends Animal implements Pet {

    // Implementing the abstract method from Animal class
    public void sound() {
        System.out.println("Dog barks");
    }
    // Implementing the play method from Pet interface
    public void play() {
        System.out.println("Dog plays");
    }
}

public class InterfaceAndAbstractClass {
    public static void main(String[] args) {
        Dog d = new Dog();
        // Calling methods from both abstract class and interface
        d.sound();
        d.sleep();
        d.play();
    }
}
