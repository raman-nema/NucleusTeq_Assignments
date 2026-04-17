package com.example.todo_application.exception;

/**
 * Exception thrown when a specific resource is not found.
 * Maps to HTTP 404 Not Found status.
 */
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String msg) {
        super(msg);
    }
}