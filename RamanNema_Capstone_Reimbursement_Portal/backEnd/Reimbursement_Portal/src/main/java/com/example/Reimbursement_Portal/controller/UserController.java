package com.example.Reimbursement_Portal.controller;

import com.example.Reimbursement_Portal.dto.Request.UserRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.UserResponseDTO;
import com.example.Reimbursement_Portal.service.UserService;

import lombok.RequiredArgsConstructor;
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
     *
     * @param request the user request data
     * @return the created user response
     */
    @PostMapping
    public UserResponseDTO createUser(@RequestBody UserRequestDTO request) {
        return userService.createUser(request);
    }

    /**
     * Retrieves all users.
     *
     * @return list of users
     */
    @GetMapping
    public List<UserResponseDTO> getAllUsers() {
        return userService.getAllUsers();
    }

    /**
     * Retrieves a user by ID.
     *
     * @param id the user ID
     * @return the user response
     */
    @GetMapping("/{id}")
    public UserResponseDTO getUserById(@PathVariable Long id) {
        return userService.getUserById(id);
    }

    /**
     * Retrieves employees under a manager.
     *
     * @param managerId the manager ID
     * @return list of employees
     */
    @GetMapping("/manager/{managerId}")
    public List<UserResponseDTO> getEmployeesByManager(@PathVariable Long managerId) {
        return userService.getEmployeesByManager(managerId);
    }

    /**
     * Deletes a user by ID.
     *
     * @param id the user ID
     * @return confirmation message
     */
    @DeleteMapping("/{id}")
    public String deleteUser(@PathVariable Long id) {
        userService.deleteUser(id);
        return "User deleted successfully with id.";
    }
}