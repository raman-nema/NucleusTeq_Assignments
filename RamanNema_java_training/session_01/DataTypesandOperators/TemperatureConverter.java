// 3)  Create a program to convert a temperature from Celsius to Fahrenheit and vice versa.
package RamanNema_java_training.session_01.DataTypesandOperators;

public class TemperatureConverter {
    // Celsius to Fahrenheit
    public double celsiusToFahrenheit(double celsius) {
        return (celsius * 9 / 5) + 32;
    }
    // Fahrenheit to Celsius
    public double fahrenheitToCelsius(double fahrenheit) {
        return (fahrenheit - 32) * 5 / 9;
    }
    public static void main(String[] args) {
        TemperatureConverter convert = new TemperatureConverter();

        double celsius = 25.0;
        double fahrenheit = convert.celsiusToFahrenheit(celsius);
        System.out.println(celsius + " °C is " + fahrenheit + " °F");

        fahrenheit = 77.0;
        celsius = convert.fahrenheitToCelsius(fahrenheit);
        System.out.println(fahrenheit + " °F is " + celsius + " °C");
    }

}
