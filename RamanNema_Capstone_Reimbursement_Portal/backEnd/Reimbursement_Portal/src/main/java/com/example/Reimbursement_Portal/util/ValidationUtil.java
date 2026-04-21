package com.example.Reimbursement_Portal.util;

public class ValidationUtil {

    // Validates that the email belongs to the company domain
    public static boolean isValidCompanyEmail(String email) {
        if (email == null) return false;

        return email.trim().toLowerCase().endsWith("@company.com");
    }
}