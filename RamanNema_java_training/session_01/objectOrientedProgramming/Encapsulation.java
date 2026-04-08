/*
3. Encapsulation in Java

Encapsulation is one of the four fundamental OOP concepts.
It means wrapping data (variables) and code (methods) together into a single unit (class).

Key Points:
1. Data members are declared as private (data hiding).
2. Access to data is provided through public getter and setter methods.
3. It ensures controlled access and improves security.

Advantages:
- Protects data from unauthorized access
- Improves code maintainability
- Allows validation before setting values
*/


// Example:  Student class demonstrating encapsulation
package RamanNema_java_training.session_01.objectOrientedProgramming;

// Student class with encapsulation
class StudentEncapsulation {
    private String name;
    private int rollNumber;
    private double marks;

    // Getter & Setter for encapsulated fields
    public String getName() { 
        return name; 
    }

    public void setName(String name) { 
        this.name = name; 
    }

    public int getRollNumber() { 
        return rollNumber; 
    }

    public void setRollNumber(int rollNumber) { 
        this.rollNumber = rollNumber; 
    }

    public double getMarks() { 
        return marks; 
    }

    public void setMarks(double marks) { 
        this.marks = marks; 
    }
}

// Main class
public class Encapsulation {
    public static void main(String[] args) {
        StudentEncapsulation s = new StudentEncapsulation();

        s.setName("Shubham");
        s.setRollNumber(101);
        s.setMarks(85);

        System.out.println("Name: " + s.getName());
        System.out.println("Roll: " + s.getRollNumber());
        System.out.println("Marks: " + s.getMarks());
    }
}