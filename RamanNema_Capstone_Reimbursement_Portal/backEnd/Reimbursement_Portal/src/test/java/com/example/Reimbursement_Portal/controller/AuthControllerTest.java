package com.example.Reimbursement_Portal.controller;

import com.example.Reimbursement_Portal.dto.Response.UserResponseDTO;
import com.example.Reimbursement_Portal.entity.User;
import com.example.Reimbursement_Portal.repository.UserRepository;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AuthControllerTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private AuthController controller;

    // ─── SUCCESS CASE ─────────────────────────────────────────────

    @Test
    void testMe_success() {

        // Mock Authentication
        Authentication authentication = mock(Authentication.class);
        when(authentication.getName()).thenReturn("test@company.com");

        // Mock User entity
        User user = new User();
        user.setId(1L);
        user.setEmail("test@company.com");
        user.setName("Shubham");

        // Mock repository
        when(userRepository.findByEmail("test@company.com"))
                .thenReturn(Optional.of(user));

        // Call controller
        ResponseEntity<?> response = controller.me(authentication);

        // Assertions
        assertNotNull(response);
        assertEquals(200, response.getStatusCode().value());

        var body = (com.example.Reimbursement_Portal.dto.StandardAPIResponse<UserResponseDTO>) response.getBody();
        assertNotNull(body);

        assertTrue(body.isSuccess());
        assertEquals("User fetched successfully", body.getMessage());

        assertNotNull(body.getData());
        assertEquals("test@company.com", body.getData().getEmail());

        verify(userRepository).findByEmail("test@company.com");
    }

    // ─── FAILURE CASE ─────────────────────────────────────────────

    @Test
    void testMe_userNotFound() {

        Authentication authentication = mock(Authentication.class);
        when(authentication.getName()).thenReturn("notfound@company.com");

        when(userRepository.findByEmail("notfound@company.com"))
                .thenReturn(Optional.empty());

        // Exception assertion
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            controller.me(authentication);
        });

        assertEquals("Logged-in user not found", exception.getMessage());

        verify(userRepository).findByEmail("notfound@company.com");
    }
}