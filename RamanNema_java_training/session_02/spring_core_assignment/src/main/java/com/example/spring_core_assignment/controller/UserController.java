package com.example.spring_core_assignment.controller;

import com.example.spring_core_assignment.model.User;
import com.example.spring_core_assignment.service.UserService;
import com.example.spring_core_assignment.service.MessageService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// REST controller for User-related APIs
@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService; // Handles user operations
    private final MessageService messageService; // Handles message formatting

    // Constructor-based dependency injection
    public UserController(UserService userService, MessageService messageService) {
        this.userService = userService;
        this.messageService = messageService;
    }

    // Get formatted message based on type (SHORT/LONG)
    @GetMapping("/message")
    public String getMessage(@RequestParam String type) {
        return messageService.getMessage(type);
    }

    // Retrieve all users
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

    // Retrieve user by ID
    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.getUserById(id);
    }

    // Trigger notification
    @GetMapping("/notify")
    public String notifyUser() {
        return userService.triggerNotification();
    }
}