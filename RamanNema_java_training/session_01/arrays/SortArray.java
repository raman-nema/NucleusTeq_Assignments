// 2)  Implement a function to sort an array in ascending order using bubble sort or selection sort.

package RamanNema_java_training.session_01.arrays;

import java.util.Scanner;

public class SortArray {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Input
        System.out.print("Enter number of elements: ");
        int n = sc.nextInt();

        if (n <= 0) {
            System.out.println("Invalid array size.");
            sc.close();
            return;
        }

        int[] arr = new int[n];

        System.out.println("Enter " + n + " elements:");
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        // Bubble Sort
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;

            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // Swap
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                }
            }

            // If no swaps happened, array is already sorted
            if (!swapped)
                break;
        }

        // Output
        System.out.println("\nSorted Array (Ascending Order):");
        for (int num : arr) {
            System.out.print(num + " ");
        }

        sc.close();
    }
}
