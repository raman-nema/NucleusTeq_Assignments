package com.example.Reimbursement_Portal.exception;

// Custom exception for invalid input
public class BadRequestException extends RuntimeException {

    public BadRequestException(String message) {
        super(message);
    }
}