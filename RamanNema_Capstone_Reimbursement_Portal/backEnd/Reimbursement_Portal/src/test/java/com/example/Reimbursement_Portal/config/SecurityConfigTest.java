package com.example.Reimbursement_Portal.config;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SecurityConfigTest {

    @Test
    void testConfigLoads() {
        SecurityConfig config = new SecurityConfig();
        assertNotNull(config);
    }
}