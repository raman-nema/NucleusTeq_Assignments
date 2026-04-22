package com.example.Reimbursement_Portal.controller;

import com.example.Reimbursement_Portal.dto.Request.UserRequest;
import com.example.Reimbursement_Portal.dto.Response.UserResponse;
import com.example.Reimbursement_Portal.service.UserService;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// REST Controller
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    // CREATE USER
    @PostMapping
    public UserResponse createUser(@RequestBody UserRequest request) {
        return userService.createUser(request);
    }

    // GET ALL USERS - retrieves all users
    @GetMapping
    public List<UserResponse> getAllUsers() {
        return userService.getAllUsers();
    }

    // GET USER BY ID - retrieves a specific user by ID
    @GetMapping("/{id}")
    public UserResponse getUserById(@PathVariable Long id) {
        return userService.getUserById(id);
    }

    // GET EMPLOYEES UNDER MANAGER - fetches users reporting to a manager
    @GetMapping("/manager/{managerId}")
    public List<UserResponse> getEmployeesByManager(@PathVariable Long managerId) {
        return userService.getEmployeesByManager(managerId);
    }

    // DELETE USER - deletes user by ID
    @DeleteMapping("/{id}")
    public String deleteUser(@PathVariable Long id) {
        userService.deleteUser(id);
        return "User deleted successfully with id.";
    }

}