// 2)  Write a program to demonstrate the use of arithmetic, logical, and relational operators.
package RamanNema_java_training.session_01.DataTypesandOperators;

public class Operators {
    // Arithmetic Operators
    public void arithmeticOper(int a, int b) {
        System.out.println("Arithmetic Operators: ");
        System.out.println("Addition: " + (a + b));
        System.out.println("Subtraction: " + (a - b));
        System.out.println("Multiplication: " + (a * b));
        System.out.println("Division: " + (a / b));
        System.out.println("Modulus: " + (a % b));
    }

    // Relational Operators
    public void relationalOper(int a, int b) {
        System.out.println("\nRelational Operators: ");
        System.out.println("a > b: " + (a > b));
        System.out.println("a < b: " + (a < b));
        System.out.println("a == b: " + (a == b));
        System.out.println("a != b: " + (a != b));
        System.out.println("a >= b: " + (a >= b));
        System.out.println("a <= b: " + (a <= b));
    }

    // Logical Operators
    public void logicalOper(int a, int b) {
        System.out.println("\nLogical Operators: ");

        boolean condition1 = (a > 0);
        boolean condition2 = (b > 0);

        System.out.println("AND (&&): " + (condition1 && condition2));
        System.out.println("OR (||): " + (condition1 || condition2));
        System.out.println("NOT (!a): " + (!condition1));
    }

    public static void main(String[] args) {
        Operators demo = new Operators();
        int a = 10;
        int b = 5;

        demo.arithmeticOper(a, b);
        demo.relationalOper(a, b);
        demo.logicalOper(a, b);
    }

}
