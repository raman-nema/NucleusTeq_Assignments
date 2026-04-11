package com.example.spring_core_assignment.controller;

import com.example.spring_core_assignment.model.User;
import com.example.spring_core_assignment.service.UserService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// REST controller for User APIs
@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService; // Service dependency

    // Constructor-based dependency injection
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // Get all users
    @GetMapping
    public List<User> getUsers() {
        return userService.getUsers();
    }

    // Add a new user
    @PostMapping
    public String addUser(@RequestBody User user) {
        userService.addUser(user);
        return "User added successfully";
    }

    // Get user by ID
    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.getUserById(id);
    }

    // Trigger notification endpoint
    @GetMapping("/notify")
    public String notifyUser() {
        return userService.triggerNotification();
    }

}