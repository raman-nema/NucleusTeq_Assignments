package com.example.Reimbursement_Portal.controller;

import com.example.Reimbursement_Portal.dto.Request.UserRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.UserResponseDTO;
import com.example.Reimbursement_Portal.dto.StandardAPIResponse;
import com.example.Reimbursement_Portal.enums.Role;
import com.example.Reimbursement_Portal.service.impl.UserServiceImpl;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import org.springframework.http.ResponseEntity;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserControllerTest {

    @Mock
    private UserServiceImpl service;

    @InjectMocks
    private UserController controller;

    // ─── Create User ─────────────────────────────────────────────

    @Test
    void testCreateUser() {

        UserRequestDTO request = new UserRequestDTO();
        request.setName("Shubham");
        request.setEmail("test@company.com");
        request.setPassword("123456");
        request.setRole(Role.ADMIN);

        UserResponseDTO userDTO = new UserResponseDTO();
        userDTO.setId(1L);
        userDTO.setName("Shubham");
        userDTO.setEmail("test@company.com");
        userDTO.setRole(Role.ADMIN);

        when(service.createUser(any())).thenReturn(userDTO);

        ResponseEntity<StandardAPIResponse<UserResponseDTO>> response =
                controller.createUser(request);

        assertNotNull(response);
        assertEquals(200, response.getStatusCode().value());

        StandardAPIResponse<UserResponseDTO> body = response.getBody();
        assertNotNull(body);

        assertEquals("User created successfully", body.getMessage());
        assertNotNull(body.getData());
        assertEquals("test@company.com", body.getData().getEmail());

        verify(service).createUser(any());
    }

    // ─── Get All Users (Non-empty) ─────────────────────────────

    @Test
    void testGetAllUsers_returnsList() {

        UserResponseDTO user = new UserResponseDTO();
        user.setEmail("test@company.com");

        when(service.getAllUsers()).thenReturn(List.of(user));

        ResponseEntity<StandardAPIResponse<List<UserResponseDTO>>> response =
                controller.getAllUsers();

        assertNotNull(response);
        assertEquals(200, response.getStatusCode().value());

        StandardAPIResponse<List<UserResponseDTO>> body = response.getBody();
        assertNotNull(body);

        assertEquals(1, body.getData().size());
        assertEquals("test@company.com", body.getData().get(0).getEmail());

        verify(service).getAllUsers();
    }

    // ─── Get All Users (Empty List) ─────────────────────────────

    @Test
    void testGetAllUsers_emptyList() {

        when(service.getAllUsers()).thenReturn(List.of());

        ResponseEntity<StandardAPIResponse<List<UserResponseDTO>>> response =
                controller.getAllUsers();

        assertNotNull(response);

        StandardAPIResponse<List<UserResponseDTO>> body = response.getBody();
        assertNotNull(body);

        assertTrue(body.getData().isEmpty());

        verify(service).getAllUsers();
    }
}