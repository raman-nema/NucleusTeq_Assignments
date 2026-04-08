
/*
4. Explore multithreading in Java to perform multiple tasks concurrently.

Multithreading in Java
- Multithreading allows multiple threads (tasks) to run concurrently
- It helps improve performance and better CPU utilization

Ways to create threads:
1. Thread class → extend Thread and override run()
2. Runnable interface → implement Runnable 

Key Methods:
- start() → starts a new thread and calls run()
- run() → contains the code to be executed by the thread

Note:
- Threads run independently and may execute in any order

Example:
*/

package RamanNema_java_training.session_01.advancedTopics;
// Using Thread class
class MyThread extends Thread {
    public void run() {
        for (int i = 1; i <= 5; i++) {
            System.out.println("Thread Class: " + i);
        }
    }
}

// Using Runnable interface
class MyRunnable implements Runnable {
    public void run() {
        for (int i = 1; i <= 5; i++) {
            System.out.println("Runnable: " + i);
        }
    }
}

// Main class
public class MultiThreading {
    public static void main(String[] args) {

        // Thread class
        MyThread t1 = new MyThread();

        // Runnable interface
        Thread t2 = new Thread(new MyRunnable());

        // Start threads
        t1.start();
        t2.start();
    }
}