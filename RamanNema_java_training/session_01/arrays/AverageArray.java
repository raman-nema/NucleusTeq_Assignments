// Arrays:
// 1)  Write a program to find the average of elements in an array.

package RamanNema_java_training.session_01.arrays;

import java.util.Scanner;

public class AverageArray {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of elements: ");
        int n = sc.nextInt();

        if (n == 0) {
            System.out.println("Array size cannot be zero.");
        }

        int[] arr = new int[n];
        int sum = 0;

        System.out.println("Enter " + n + " elements:");
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
            sum += arr[i];
        }

        double average = (double) sum / n;

        System.out.printf("Average: %.2f\n", average);

        sc.close();
    }
}
