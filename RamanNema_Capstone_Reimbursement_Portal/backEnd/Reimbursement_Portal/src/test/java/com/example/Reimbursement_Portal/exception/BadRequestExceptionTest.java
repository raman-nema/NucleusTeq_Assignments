package com.example.Reimbursement_Portal.exception;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class BadRequestExceptionTest {

    @Test
    void testExceptionMessage() {

        BadRequestException ex =
                new BadRequestException("Invalid request");

        assertEquals("Invalid request", ex.getMessage());
    }
}