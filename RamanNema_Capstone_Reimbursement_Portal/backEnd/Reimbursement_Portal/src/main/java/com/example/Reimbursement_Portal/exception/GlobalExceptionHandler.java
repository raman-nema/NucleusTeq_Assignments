package com.example.Reimbursement_Portal.exception;

import com.example.Reimbursement_Portal.dto.StandardAPIResponse;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@ControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(BadRequestException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleBadRequest(BadRequestException ex) {
        log.error("Bad Request Error: {}", ex.getMessage());
        return ResponseEntity.badRequest().body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message(ex.getMessage())
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity.status(404).body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message(ex.getMessage())
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleDataIntegrity(DataIntegrityViolationException ex) {
        return ResponseEntity.badRequest().body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message("Cannot delete this user because they have existing claims in the system. Please delete their claims first.")
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleGeneric(Exception ex) {
        log.error("Something went wrong", ex);
        return ResponseEntity.internalServerError().body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message("Something went wrong: " + ex.getMessage())
                        .data(null)
                        .build()
        );
    }

}