package RamanNema_java_training.session_01.basic;

import java.util.Scanner;

public class AreaCalculator {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Displaying menu options
        System.out.println("Choose shape:");
        System.out.println("1. Circle");
        System.out.println("2. Rectangle");
        System.out.println("3. Triangle");

        System.out.print("Enter your choice: ");
        int choice = sc.nextInt();

        switch (choice) {

            case 1:
                // Area of Circle = π * r * r
                System.out.print("Enter radius: ");
                double radius = sc.nextDouble();

                double circleArea = Math.PI * radius * radius;
                System.out.println("Area of Circle: " + circleArea);
                break;

            case 2:
                // Area of Rectangle = length * width
                System.out.print("Enter length: ");
                double length = sc.nextDouble();

                System.out.print("Enter width: ");
                double width = sc.nextDouble();

                double rectangleArea = length * width;
                System.out.println("Area of Rectangle: " + rectangleArea);
                break;

            case 3:
                // Area of Triangle = 0.5 * base * height
                System.out.print("Enter base: ");
                double base = sc.nextDouble();

                System.out.print("Enter height: ");
                double height = sc.nextDouble();

                double triangleArea = 0.5 * base * height;
                System.out.println("Area of Triangle: " + triangleArea);
                break;

            default:
                // Invalid input
                System.out.println("Invalid choice!");
        }

        sc.close();
    }
}