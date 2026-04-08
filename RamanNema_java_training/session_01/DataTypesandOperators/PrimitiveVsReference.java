/*
    Data Types and Operators:
  1.) Difference between Primitive and Reference Data Types in Java
 
  a. Primitive Data Types:
    - These store actual values directly in memory.
    - They are predefined by Java.
    - They have fixed size.
    - Stored in stack memory.
    - Examples: int, float, char, boolean

     Example:
         int a = 10;
         char c = 'A';
 
  b. Reference Data Types:
    - These store the reference (memory address) of objects.
    - Objects are stored in heap memory.
    - They can hold complex data.
    - Can be null.
    - Created using 'new' keyword (in most cases).
 
     Examples:
        String name = "Shubham";
        int[] arr = {1, 2, 3};
        PrimeChecker obj = new PrimeChecker();
 
  Key Differences:
    - Primitive → stores actual value
    - Reference → stores address of object

    - Primitive → stack memory
    - Reference → heap memory
 
    - Primitive → fixed size
    - Reference → variable size
 */


package RamanNema_java_training.session_01.DataTypesandOperators;
public class PrimitiveVsReference {
    public static void main(String[] args) {
        System.out.println("Check comments for explanation.");
    }
}