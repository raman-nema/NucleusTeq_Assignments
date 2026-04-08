// 4)  Create a program to calculate the sum of even numbers from 1 to 10 using a while loop.

package RamanNema_java_training.session_01.controlFlow;

import java.util.Scanner;

public class SumEvenNumbers {
    public static void main(String[] args) {
        System.out.print("Enter the start and end range to calculate the sum of even numbers: ");
        Scanner sc = new Scanner(System.in);
        int i= sc.nextInt();
        int start = i;
        int end = sc.nextInt();
        int sum = 0;
        while (start <= end) {
            if (start % 2 == 0) {
                sum += start;
            }
            start++;
        }
        System.out.println("Sum of even numbers from " + i + " to " + end + " is: " + sum);

        sc.close();
    }
}
