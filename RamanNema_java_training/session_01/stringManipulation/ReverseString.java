// String Manipulation:
// 1. Write a program to reverse a given string.

package RamanNema_java_training.session_01.stringManipulation;
import java.util.Scanner;
public class ReverseString {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        // Enter a string from the user
        System.out.print("Enter a string: ");
        String str = sc.nextLine();

        String reversed = "";
        // Loop through the string in reverse order and build the reversed string
        for (int i = str.length() - 1; i >= 0; i--) {
            reversed += str.charAt(i);
        }

        System.out.println("Reversed String: " + reversed);
        sc.close();
    }
}
