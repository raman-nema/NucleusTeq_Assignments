package com.example.Reimbursement_Portal.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for the ValidationUtil class.
 * We check if the email validation works correctly.
 *
 */
class ValidationUtilTest {

    @Test
    void testValidCompanyEmail_shouldReturnTrue() {
        // A proper company email should pass
        assertTrue(ValidationUtil.isValidCompanyEmail("alice@company.com"));
    }

    @Test
    void testValidCompanyEmailWithSpaces_shouldReturnTrue() {
        // Emails with leading/trailing spaces should still pass after trim
        assertTrue(ValidationUtil.isValidCompanyEmail("  bob@company.com  "));
    }

    @Test
    void testGmailEmail_shouldReturnFalse() {
        // Gmail is not a company email
        assertFalse(ValidationUtil.isValidCompanyEmail("alice@gmail.com"));
    }

    @Test
    void testNullEmail_shouldReturnFalse() {
        // Null email should not crash, just return false
        assertFalse(ValidationUtil.isValidCompanyEmail(null));
    }

    @Test
    void testEmptyEmail_shouldReturnFalse() {
        // Empty string is not valid
        assertFalse(ValidationUtil.isValidCompanyEmail(""));
    }

    @Test
    void testEmailWithUpperCase_shouldReturnTrue() {
        // Upper case should still match since we do toLowerCase()
        assertTrue(ValidationUtil.isValidCompanyEmail("ALICE@COMPANY.COM"));
    }

}