package com.example.spring_core_assignment.repository;

import com.example.spring_core_assignment.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;

// In-memory repository for User data
@Repository
public class UserRepository {

    private final List<User> users = new ArrayList<>(); // Storage

    // Return all users
    public List<User> findAll() {
        return users;
    }

    // Save user
    public void save(User user) {
        users.add(user);
    }

    // Find user by ID
    public User findById(Long id) {
        return users.stream()
                .filter(user -> user.getId().equals(id))
                .findFirst()
                .orElse(null);
    }
}