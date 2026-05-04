package com.example.Reimbursement_Portal.mapper;

import com.example.Reimbursement_Portal.dto.Request.ClaimRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.ClaimResponseDTO;
import com.example.Reimbursement_Portal.entity.Claim;
import com.example.Reimbursement_Portal.entity.User;
import com.example.Reimbursement_Portal.enums.ClaimStatus;
import com.example.Reimbursement_Portal.enums.Role;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for ClaimMapper.
 * Ensures claims are correctly converted between Entity and DTO.
 */
class ClaimMapperTest {

    // ─── toResponse() tests ───────────────────────────────────

    @Test
    void testToResponse_withEmployeeAndReviewer() {
        // GIVEN: Employee and reviewer users
        User employee = new User();
        employee.setId(1L);
        employee.setName("Alice Employee");

        User reviewer = new User();
        reviewer.setId(2L);
        reviewer.setName("Bob Manager");

        // GIVEN: A claim linked to both
        Claim claim = new Claim();
        claim.setId(100L);
        claim.setAmount(2500.0);
        claim.setDescription("Office supplies");
        claim.setDate(LocalDate.of(2024, 6, 15));
        claim.setStatus(ClaimStatus.SUBMITTED);
        claim.setEmployee(employee);
        claim.setReviewer(reviewer);
        claim.setComment("Looks good");

        // WHEN: Convert to DTO
        ClaimResponseDTO dto = ClaimMapper.toResponse(claim);

        // THEN: All fields should be correctly mapped
        assertEquals(100L, dto.getId());
        assertEquals(2500.0, dto.getAmount());
        assertEquals("Office supplies", dto.getDescription());
        assertEquals(ClaimStatus.SUBMITTED, dto.getStatus());
        assertEquals(1L, dto.getEmployeeId());
        assertEquals("Alice Employee", dto.getEmployeeName());
        assertEquals(2L, dto.getReviewerId());
        assertEquals("Bob Manager", dto.getReviewerName());
        assertEquals("Looks good", dto.getComment());
    }


    @Test
    void testToResponse_withNoEmployee() {
        // GIVEN: Claim with null employee (edge case)
        Claim claim = new Claim();
        claim.setId(300L);
        claim.setAmount(100.0);
        claim.setDescription("Test");
        claim.setStatus(ClaimStatus.APPROVED);
        claim.setEmployee(null);
        claim.setReviewer(null);

        // WHEN + THEN: Should not crash; employee fields should be null
        ClaimResponseDTO dto = ClaimMapper.toResponse(claim);
        assertNull(dto.getEmployeeId());
        assertNull(dto.getEmployeeName());
    }

    // ─── toEntity() tests ─────────────────────────────────────

    @Test
    void testToEntity_setsAllFields() {
        // GIVEN: A claim request from frontend
        ClaimRequestDTO request = new ClaimRequestDTO();
        request.setAmount(1500.0);
        request.setDescription("Laptop charger");
        request.setEmployeeId(1L);

        User employee = new User();
        employee.setId(1L);

        User reviewer = new User();
        reviewer.setId(2L);

        // WHEN: Convert to entity
        Claim claim = ClaimMapper.toEntity(request, employee, reviewer);

        // THEN: All fields should be set correctly
        assertEquals(1500.0, claim.getAmount());
        assertEquals("Laptop charger", claim.getDescription());
        assertEquals(ClaimStatus.SUBMITTED, claim.getStatus()); // should default to SUBMITTED
        assertEquals(employee, claim.getEmployee());
        assertEquals(reviewer, claim.getReviewer());
    }
}