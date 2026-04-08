package RamanNema_java_training.session_01.basic;

public class PatternPrinting {
    public static void main(String[] args) {

        // Triangle Pattern
        System.out.println("Triangle Pattern print:");
        // Outer loop controls rows
        for (int i = 1; i <= 5; i++) {
            // Inner loop prints stars
            for (int j = 1; j <= i; j++) {
                System.out.print("* ");
            }
            // Move to next line after each row
            System.out.println();
        }

        // Square Pattern
        System.out.println("\nSquare Pattern print:");

        // Outer loop for rows
        for (int i = 1; i <= 5; i++) {
            // Inner loop for columns
            for (int j = 1; j <= 5; j++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }
}
