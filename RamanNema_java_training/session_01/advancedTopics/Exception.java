/*
02. Exception Handling in Java

- Used to handle runtime errors and prevent program crash

Keywords:
try   → contains risky code
catch → handles the exception
finally → always executes

Flow:
- try block runs
- If error occurs → catch block handles it
- Program continues normally

Example:
*/


package RamanNema_java_training.session_01.advancedTopics;

public class Exception {
    public static void main(String[] args) {

        // Example of try-catch for handling ArithmeticException
        try {
            int a = 10;
            int b = 0;

            // Risky operation (may cause exception)
            int result = a / b;

            System.out.println("Result: " + result);

        } catch (ArithmeticException e) {
            // Handles division by zero error
            System.out.println("Error: Cannot divide by zero");
        }

        // This will always execute after try-catch
        System.out.println("Program continues...");
    }
}

