// Control Flow Statements:
// 1)  Write a program to check if a given number is prime using an if-else statement.

package RamanNema_java_training.session_01.controlFlow;

import java.util.Scanner;

public class PrimeChecker {
    public boolean isPrime(int number) {
        if (number <= 1) {
            return false;
        } else {
            for (int i = 2; i <= Math.sqrt(number); i++) {
                if (number % i == 0) {
                    return false;
                }
            }
            return true;
        }
    }

    public static void main(String[] args) {
        System.out.print("Enter a number to check if it's prime: ");
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        PrimeChecker pC = new PrimeChecker();
        boolean isPrime = pC.isPrime(n);
        if (isPrime) {
            System.out.println(n + " is a prime number.");
        } else {
            System.out.println(n + " is not a prime number.");
        }
        sc.close();
    }
}
