// 2. Implement a function to count the number of vowels in a string. 

package RamanNema_java_training.session_01.stringManipulation;
import java.util.Scanner;
public class CountVowels {
    // Function to count vowels
    public static int vowelCount(String str) {
        int count = 0;

        // Convert the string to lowercase to handle both uppercase and lowercase vowels
        str = str.toLowerCase();

        // Loop through each character in the string and check if it's a vowel
        for (int i = 0; i < str.length(); i++) {
            char ch = str.charAt(i);

            if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {
                count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter a string: ");
        String st = sc.nextLine();
        int result = vowelCount(st);
        System.out.println("Number of vowels: " + result);

        sc.close();
    }
}