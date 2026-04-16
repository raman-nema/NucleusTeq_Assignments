/*
3. Implement a simple file I/O operation to read data from a text file. 

    This program demonstrates basic file input operations in Java. It reads a line from a file named "test.txt" and prints it to the console. The program uses a BufferedReader wrapped around a FileReader to read the file. If any exceptions occur during the file reading process, it catches the exception and prints an error message.
    Location of the file : test.txt should be in the same directory as the compiled class file or you can provide an absolute path to the file.
*/ 

package RamanNema_java_training.session_01.advancedTopics;
import java.io.*;

public class IO_operations {
    public static void main(String[] args) {

        // Reading from a file
        try {
           BufferedReader br = new BufferedReader(
    new FileReader("/Users/ramannema/Documents/NT/NucleusTeq_Assignments/RamanNema_java_training/session_01/advancedTopics/test.txt")
);
            // Read a line from the file
            String line = br.readLine();
            System.out.println(line);

            // Close the reader
            br.close();

        }
        // Catch any exceptions that occur during file reading
        catch (java.lang.Exception e) {
            System.out.println("Error reading file");
        }
    }
}
