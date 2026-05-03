package com.example.Reimbursement_Portal.exception;

import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.*;

class GlobalExceptionHandlerTest {

    private final GlobalExceptionHandler handler = new GlobalExceptionHandler();

    @Test
    void testBadRequestException() {

        BadRequestException ex = new BadRequestException("Invalid data");

        ResponseEntity<?> response = handler.handleBadRequest(ex);

        assertEquals(400, response.getStatusCode().value());
    }

    @Test
    void testResourceNotFoundException() {

        ResourceNotFoundException ex = new ResourceNotFoundException("Not found");

        ResponseEntity<?> response = handler.handleNotFound(ex);

        assertEquals(404, response.getStatusCode().value());
    }
}