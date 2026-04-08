package RamanNema_java_training.session_01.basic;

import java.util.Scanner;

public class Fibonacci {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Ask user for number of terms
        System.out.print("Enter number of terms: ");
        int n = sc.nextInt();

        int firstTerm = 0, secondTerm = 1;

        System.out.println("Fibonacci Sequence:");

        // Loop to print Fibonacci series
        for (int i = 1; i <= n; i++) {
            System.out.print(firstTerm + " ");

            // Calculate next term
            int next = firstTerm + secondTerm;
            firstTerm = secondTerm;
            secondTerm = next;
        }

        sc.close();
    }
}
