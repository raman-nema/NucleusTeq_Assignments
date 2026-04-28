package com.example.Reimbursement_Portal.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.MethodArgumentNotValidException;

/**
 * Global exception handler for REST APIs.
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * Handles bad request exceptions.
     *
     * @param ex the exception
     * @return error response
     */
    @ExceptionHandler(BadRequestException.class)
    public ResponseEntity<String> handleBadRequest(BadRequestException ex) {
        return new ResponseEntity<>(ex.getMessage(), HttpStatus.BAD_REQUEST);
    }

    /**
     * Handles resource not found exceptions.
     *
     * @param ex the exception
     * @return error response
     */
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<?> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(ex.getMessage());
    }

    /**
     * Handles validation exceptions.
     *
     * @param ex the exception
     * @return error response
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<String> handleValidationException(MethodArgumentNotValidException ex) {

        String errorMessage = ex.getBindingResult()
                .getFieldErrors()
                .stream()
                .findFirst()
                .map(error -> error.getDefaultMessage())
                .orElse("Validation error");

        return new ResponseEntity<>(errorMessage, HttpStatus.BAD_REQUEST);
    }
}