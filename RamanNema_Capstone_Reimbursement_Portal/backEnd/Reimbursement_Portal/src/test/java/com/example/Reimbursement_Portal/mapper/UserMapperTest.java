package com.example.Reimbursement_Portal.mapper;

import com.example.Reimbursement_Portal.dto.Request.UserRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.UserResponseDTO;
import com.example.Reimbursement_Portal.entity.User;
import com.example.Reimbursement_Portal.enums.Role;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for UserMapper.
 * Mapper converts between Entity (database object) and DTO (API object).
 *
 * Think of it like a translator between two languages.
 */
class UserMapperTest {

    // ─── toResponse() tests ───────────────────────────────────

    @Test
    void testToResponse_basicFields() {
        // GIVEN: A user in the database
        User user = new User();
        user.setId(1L);
        user.setName("Alice");
        user.setEmail("alice@company.com");
        user.setRole(Role.EMPLOYEE);
        user.setManager(null); // no manager

        // WHEN: We convert it to a response DTO
        UserResponseDTO dto = UserMapper.toResponse(user);

        // THEN: All fields should match
        assertEquals(1L, dto.getId());
        assertEquals("Alice", dto.getName());
        assertEquals("alice@company.com", dto.getEmail());
        assertEquals(Role.EMPLOYEE, dto.getRole());
        assertNull(dto.getManagerId());
        assertNull(dto.getManagerName());
    }

    // ─── toEntity() tests ─────────────────────────────────────

    @Test
    void testToEntity_basicConversion() {
        // GIVEN: A request from the frontend/API
        UserRequestDTO request = new UserRequestDTO();
        request.setName("Dave");
        request.setEmail("dave@company.com");
        request.setPassword("secret123");
        request.setRole(Role.MANAGER);

        String encryptedPassword = "bcrypt_hashed_password";

        // WHEN: We create a User entity from it
        User user = UserMapper.toEntity(request, encryptedPassword);

        // THEN: Entity should have the right fields
        assertEquals("Dave", user.getName());
        assertEquals("dave@company.com", user.getEmail());
        assertEquals(encryptedPassword, user.getPassword()); // must use encrypted password
        assertEquals(Role.MANAGER, user.getRole());
    }

    @Test
    void testToEntity_withNullRequest_returnsNull() {
        // GIVEN: A null request (defensive programming test)
        // WHEN + THEN: Should return null instead of crashing
        User user = UserMapper.toEntity(null, "somePassword");
        assertNull(user);
    }




    @Test
    void user_noArgsConstructor() {
        User user = new User();
        assertThat(user.getId()).isNull();
        assertThat(user.getName()).isNull();
    }




}