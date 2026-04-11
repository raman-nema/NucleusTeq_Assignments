package com.example.spring_core_assignment.exception;

// Custom exception for user not found scenarios
public class UserNotFoundException extends RuntimeException {

    // Constructor to pass custom error message
    public UserNotFoundException(String message) {
        super(message);
    }
}