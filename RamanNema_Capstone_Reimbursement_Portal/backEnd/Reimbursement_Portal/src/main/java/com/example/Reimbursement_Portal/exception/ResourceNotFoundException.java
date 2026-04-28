package com.example.Reimbursement_Portal.exception;

/**
 * Exception for resource not found.
 */
public class ResourceNotFoundException extends RuntimeException {

    /**
     * Constructs a new ResourceNotFoundException.
     *
     * @param message the error message
     */
    public ResourceNotFoundException(String message) {
        super(message);
    }
}