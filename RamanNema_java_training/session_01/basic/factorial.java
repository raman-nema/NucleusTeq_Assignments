package RamanNema_java_training.session_01.basic;

import java.util.Scanner;

public class factorial {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Ask user for input
        System.out.print("Enter a number: ");
        int num = sc.nextInt();

        int factorial = 1;

        // Check if number is negative
        if (num < 0) {
            System.out.println("Factorial is not defined for negative numbers.");
        } else {
            // Loop to calculate factorial
            for (int i = 1; i <= num; i++) {
                factorial = factorial * i; // multiply each number
            }

            // Display result
            System.out.println("Factorial of " + num + " is: " + factorial);
        }

        sc.close();
    }
}

