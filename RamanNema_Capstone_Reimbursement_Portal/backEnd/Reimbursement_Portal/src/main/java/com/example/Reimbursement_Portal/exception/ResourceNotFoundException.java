package com.example.Reimbursement_Portal.exception;

// Exception thrown when a requested resource is not found
public class ResourceNotFoundException extends RuntimeException {

    // Constructor to pass error message
    public ResourceNotFoundException(String message) {
        super(message);
    }
}