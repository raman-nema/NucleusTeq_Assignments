package com.example.spring_core_assignment.service;

import com.example.spring_core_assignment.model.User;
import com.example.spring_core_assignment.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;

// Service layer for User operations
@Service
public class UserService {

    private final UserRepository userRepository; // Repository dependency

    // Constructor-based dependency injection
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // Get all users
    public List<User> getUsers() {
        return userRepository.findAll();
    }

    // Add a new user
    public void addUser(User user) {
        userRepository.save(user);
    }

    // Get user by ID
    public User getUserById(Long id) {
        return userRepository.findById(id);
    }
}