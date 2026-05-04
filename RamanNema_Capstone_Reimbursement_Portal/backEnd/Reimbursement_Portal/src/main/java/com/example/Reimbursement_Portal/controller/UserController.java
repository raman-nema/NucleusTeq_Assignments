package com.example.Reimbursement_Portal.controller;

import com.example.Reimbursement_Portal.dto.Request.UserRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.UserResponseDTO;
import com.example.Reimbursement_Portal.dto.StandardAPIResponse;
import com.example.Reimbursement_Portal.service.UserService;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controller for managing user operations.
 */
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    /**
     * Creates a new user.
     */
    @PostMapping
    public ResponseEntity<StandardAPIResponse<UserResponseDTO>> createUser(
            @RequestBody UserRequestDTO request) {

        UserResponseDTO response = userService.createUser(request);

        StandardAPIResponse<UserResponseDTO> apiResponse =
                StandardAPIResponse.<UserResponseDTO>builder()
                        .success(true)
                        .message("User created successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    /**
     * Retrieves all users.
     */
    @GetMapping
    public ResponseEntity<StandardAPIResponse<List<UserResponseDTO>>> getAllUsers() {

        List<UserResponseDTO> response = userService.getAllUsers();

        StandardAPIResponse<List<UserResponseDTO>> apiResponse =
                StandardAPIResponse.<List<UserResponseDTO>>builder()
                        .success(true)
                        .message("Users fetched successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    /**
     * Retrieves a user by ID.
     */
    @GetMapping("/{id}")
    public ResponseEntity<StandardAPIResponse<UserResponseDTO>> getUserById(
            @PathVariable Long id) {

        UserResponseDTO response = userService.getUserById(id);

        StandardAPIResponse<UserResponseDTO> apiResponse =
                StandardAPIResponse.<UserResponseDTO>builder()
                        .success(true)
                        .message("User fetched successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    /**
     * Retrieves employees under a manager.
     */
    @GetMapping("/manager/{managerId}")
    public ResponseEntity<StandardAPIResponse<List<UserResponseDTO>>> getEmployeesByManager(
            @PathVariable Long managerId) {

        List<UserResponseDTO> response = userService.getEmployeesByManager(managerId);

        StandardAPIResponse<List<UserResponseDTO>> apiResponse =
                StandardAPIResponse.<List<UserResponseDTO>>builder()
                        .success(true)
                        .message("Employees fetched successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    /**
     * Deletes a user by ID.
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<StandardAPIResponse<String>> deleteUser(@PathVariable Long id) {

        userService.deleteUser(id);

        StandardAPIResponse<String> apiResponse =
                StandardAPIResponse.<String>builder()
                        .success(true)
                        .message("User deleted successfully")
                        .data("User deleted with id: " + id)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }
}